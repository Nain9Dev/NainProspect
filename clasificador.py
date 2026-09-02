"""Lead classification with Claude Haiku 4.5.

Reads the raw leads CSV, asks the model for a compact JSON verdict per lead,
and writes leads_enriquecidos.csv. Handles rate limits with exponential
backoff and never loses a lead: a failed classification is written with
estado=error so the row survives for a later retry.
"""

import csv
import json
import random
import re
import time

import config
from scraping import LEAD_FIELDS

MAX_OUTPUT_TOKENS = 150
MAX_RETRIES = 5
BASE_BACKOFF_SECONDS = 2

CLASSIFICATION_FIELDS = [
    "industria",
    "tamano_estimado",
    "prioridad",
    "confianza",
    "motivo",
    "estado",
]

OUTPUT_FIELDS = LEAD_FIELDS + CLASSIFICATION_FIELDS

INDUSTRIES = ["logistica", "tecnologia", "retail", "industrial", "alimentacion", "otro"]

SYSTEM_PROMPT = (
    "You classify B2B sales leads. Answer with a single JSON object and no "
    "other text. Schema: {\"industria\": one of "
    "[logistica, tecnologia, retail, industrial, alimentacion, otro], "
    "\"tamano_estimado\": one of [micro, pequena, mediana, grande, desconocido], "
    "\"prioridad\": integer 1-5, \"confianza\": one of [alta, media, baja], "
    "\"motivo\": at most 15 words in Spanish}. "
    "Target profile: companies between 50 and 500 employees in Spain or Latin "
    "America. Give priority 5 only when the size band clearly matches and the "
    "company has a usable contact channel. When headcount is unknown, set "
    "tamano_estimado to your best guess and confianza to baja."
)


def build_user_prompt(lead):
    """Build the compact per-lead prompt."""
    return (
        "Nombre: {nombre}\n"
        "Web: {web}\n"
        "Email: {email}\n"
        "Ciudad: {ciudad}\n"
        "Pais: {pais}\n"
        "Categoria de origen: {categoria}\n"
        "Empleados declarados: {empleados}"
    ).format(
        nombre=lead.get("nombre", ""),
        web=lead.get("web", ""),
        email=lead.get("email", ""),
        ciudad=lead.get("ciudad", ""),
        pais=lead.get("pais", ""),
        categoria=lead.get("categoria_origen", ""),
        empleados=lead.get("empleados_declarados") or "desconocido",
    )


def parse_verdict(raw_text):
    """Parse the model answer into a normalised dict.

    Tolerates a JSON object wrapped in stray text, which is the realistic
    failure mode for a small model with a tight token budget.
    """
    match = re.search(r"\{.*\}", raw_text or "", re.DOTALL)
    if not match:
        raise ValueError("no JSON object in model answer")

    data = json.loads(match.group(0))

    industria = str(data.get("industria", "otro")).lower().strip()
    if industria not in INDUSTRIES:
        industria = "otro"

    try:
        prioridad = int(data.get("prioridad", 1))
    except (TypeError, ValueError):
        prioridad = 1
    prioridad = max(1, min(5, prioridad))

    confianza = str(data.get("confianza", "baja")).lower().strip()
    if confianza not in ("alta", "media", "baja"):
        confianza = "baja"

    return {
        "industria": industria,
        "tamano_estimado": str(data.get("tamano_estimado", "desconocido")).lower().strip(),
        "prioridad": prioridad,
        "confianza": confianza,
        "motivo": str(data.get("motivo", ""))[:200],
        "estado": "ok",
    }


def classify_simulated(lead):
    """Deterministic offline classifier used when no API key is present."""
    haystack = " ".join([
        lead.get("nombre", ""),
        lead.get("categoria_origen", ""),
        lead.get("web", ""),
    ]).lower()

    if any(word in haystack for word in ("logist", "transport", "almacen", "distribu")):
        industria = "logistica"
    elif any(word in haystack for word in ("tecno", "software", "nube", "sistemas", "it")):
        industria = "tecnologia"
    elif any(word in haystack for word in ("retail", "tienda", "moda", "comercio")):
        industria = "retail"
    elif any(word in haystack for word in ("aliment", "food")):
        industria = "alimentacion"
    elif any(word in haystack for word in ("ferret", "industrial", "suministro")):
        industria = "industrial"
    else:
        industria = "otro"

    raw_headcount = lead.get("empleados_declarados")
    try:
        headcount = int(raw_headcount)
    except (TypeError, ValueError):
        headcount = None

    if headcount is None:
        tamano, prioridad, confianza = "desconocido", 2, "baja"
    elif headcount < config.TARGET_MIN_EMPLOYEES:
        tamano, prioridad, confianza = "pequena", 1, "alta"
    elif headcount > config.TARGET_MAX_EMPLOYEES:
        tamano, prioridad, confianza = "grande", 2, "alta"
    else:
        tamano, confianza = "mediana", "alta"
        prioridad = 5 if lead.get("email") else 4

    return {
        "industria": industria,
        "tamano_estimado": tamano,
        "prioridad": prioridad,
        "confianza": confianza,
        "motivo": "Clasificacion heuristica local, sin llamada al modelo.",
        "estado": "simulado",
    }


def classify_with_haiku(client, lead, usage_accumulator):
    """Classify one lead, retrying on transient API errors."""
    import anthropic

    for attempt in range(MAX_RETRIES):
        try:
            message = client.messages.create(
                model=config.HAIKU_MODEL,
                max_tokens=MAX_OUTPUT_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": build_user_prompt(lead)}],
            )
            usage_accumulator["input_tokens"] += message.usage.input_tokens
            usage_accumulator["output_tokens"] += message.usage.output_tokens
            return parse_verdict(message.content[0].text)

        except (anthropic.RateLimitError, anthropic.APIConnectionError,
                anthropic.InternalServerError) as error:
            if attempt == MAX_RETRIES - 1:
                return _error_verdict(error)
            delay = BASE_BACKOFF_SECONDS * (2 ** attempt) + random.uniform(0, 1)
            print("  Reintento en {0:.1f}s tras {1}".format(delay, type(error).__name__))
            time.sleep(delay)

        except (ValueError, json.JSONDecodeError, IndexError, KeyError) as error:
            # Malformed answer: one retry is worth it, then give up on this lead.
            if attempt >= 1:
                return _error_verdict(error)
            time.sleep(BASE_BACKOFF_SECONDS)

        except anthropic.APIStatusError as error:
            # 4xx other than rate limit: retrying will not help.
            return _error_verdict(error)

    return _error_verdict(RuntimeError("retries exhausted"))


def _error_verdict(error):
    """Build the placeholder verdict written when classification fails."""
    return {
        "industria": "otro",
        "tamano_estimado": "desconocido",
        "prioridad": 1,
        "confianza": "baja",
        "motivo": "Error de clasificacion: " + type(error).__name__,
        "estado": "error",
    }


def leer_leads(path=None):
    """Read the raw leads CSV into a list of dicts."""
    origin = path or config.LEADS_RAW_CSV
    with open(origin, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def clasificar_leads(leads, verbose=True):
    """Classify every lead and return (rows, usage)."""
    usage = {"input_tokens": 0, "output_tokens": 0}
    client = None

    if not config.classification_is_simulated():
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    rows = []
    for index, lead in enumerate(leads, start=1):
        if client is None:
            verdict = classify_simulated(lead)
        else:
            verdict = classify_with_haiku(client, lead, usage)

        row = dict(lead)
        row.update(verdict)
        rows.append(row)

        if verbose:
            print("[{0}/{1}] {2} -> {3} / {4} / prioridad {5}".format(
                index, len(leads), lead.get("nombre", "?"),
                verdict["industria"], verdict["tamano_estimado"], verdict["prioridad"]
            ))

    return rows, usage


def estimar_coste(usage, leads_procesados):
    """Return the observed cost and the extrapolation to 100 leads."""
    input_cost = usage["input_tokens"] / 1_000_000 * config.HAIKU_INPUT_COST_PER_MTOK
    output_cost = usage["output_tokens"] / 1_000_000 * config.HAIKU_OUTPUT_COST_PER_MTOK
    total = input_cost + output_cost
    per_lead = total / leads_procesados if leads_procesados else 0.0
    return {
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "coste_usd": round(total, 6),
        "coste_por_lead_usd": round(per_lead, 6),
        "coste_100_leads_usd": round(per_lead * 100, 4),
    }


def guardar_enriquecidos(rows, path=None):
    """Write the classified leads and return the path used."""
    config.ensure_directories()
    destination = path or config.LEADS_ENRICHED_CSV
    with open(destination, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return destination


if __name__ == "__main__":
    print("Modo: " + config.describe_mode())
    entrada = leer_leads()
    resultado, consumo = clasificar_leads(entrada)
    ruta = guardar_enriquecidos(resultado)
    print("Guardado en: " + str(ruta))
    print("Coste: " + json.dumps(estimar_coste(consumo, len(entrada))))
