"""Lead classification engine with Claude Haiku 4.5 and deterministic rule fallback."""

import json
import os
import re
from typing import Tuple
from src.nainprospect.domain.models import (
    RawLead,
    EnrichedLead,
    CostMetrics,
    IndustryType,
    SizeBandType,
    ConfidenceType,
)

HAIKU_MODEL = "claude-haiku-4-5-20251001"
HAIKU_INPUT_COST_PER_MTOK = 1.0
HAIKU_OUTPUT_COST_PER_MTOK = 5.0

SECTOR_KEYWORDS = {
    "logistica": ["transporte", "logistica", "almacen", "distribucion", "flota", "envios", "carga"],
    "tecnologia": ["software", "sistemas", "cloud", "saas", "desarrollo", "tech"],
    "retail": ["tienda", "retail", "comercio", "textil", "moda", "venta al por menor"],
    "industrial": ["industrial", "fabricacion", "suministro", "taller", "mecanica", "tornilleria"],
    "alimentacion": ["alimentos", "alimentacion", "comida", "bebida", "conservas", "envasado"],
}


def rule_based_classify(lead: RawLead) -> Tuple[IndustryType, SizeBandType, int, ConfidenceType, str]:
    """Deterministic classification fallback when LLM is unavailable."""
    text_corpus = f"{lead.nombre} {lead.categoria_origen}".lower()

    # Determine industry using word-boundary matching
    matched_industry: IndustryType = "otro"
    for ind, keywords in SECTOR_KEYWORDS.items():
        pattern = r"\b(" + "|".join(re.escape(kw) for kw in keywords) + r")\b"
        if re.search(pattern, text_corpus):
            matched_industry = ind  # type: ignore[assignment]
            break

    # Determine size
    headcount = lead.empleados_declarados
    confidence: ConfidenceType = "alta" if headcount is not None else "media"

    if headcount is not None:
        if headcount < 10:
            size: SizeBandType = "micro"
        elif headcount < 50:
            size = "pequena"
        elif headcount <= 500:
            size = "mediana"
        else:
            size = "grande"
    else:
        size = "mediana"
        confidence = "baja"

    # Determine priority (target: 50-500 employees, verified corporate email)
    if size == "mediana" and lead.email:
        priority = 5
        reason = "Empresa en rango objetivo 50-500 con canal de contacto verificado"
    elif size == "mediana" and not lead.email:
        priority = 4
        reason = "Tamano objetivo pero requiere localizar buzon de rol corporativo"
    elif size in ("pequena", "micro"):
        priority = 2
        reason = "Headcount inferior a 50 empleados (fuera del objetivo prioritario)"
    else:
        priority = 1
        reason = "Gran corporacion (>500) o sector no alineado"

    return matched_industry, size, priority, confidence, reason


def classify_lead_with_llm(lead: RawLead, api_key: str) -> Tuple[IndustryType, SizeBandType, int, ConfidenceType, str, int, int]:
    """Classify lead using Claude Haiku 4.5."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You classify B2B sales leads. Answer with a single JSON object and no other text. "
        "Schema: {\"industria\": one of [logistica, tecnologia, retail, industrial, alimentacion, otro], "
        "\"tamano_estimado\": one of [micro, pequena, mediana, grande, desconocido], "
        "\"prioridad\": integer 1-5, \"confianza\": one of [alta, media, baja], "
        "\"motivo\": at most 15 words in Spanish}. "
        "Target profile: companies between 50 and 500 employees. "
        "Assign priority 5 only when size matches and role email is present."
    )

    user_prompt = (
        f"Nombre: {lead.nombre}\nWeb: {lead.web}\nEmail: {lead.email or 'sin email'}\n"
        f"Ciudad: {lead.ciudad}\nPais: {lead.pais}\nCategoria: {lead.categoria_origen}\n"
        f"Empleados declarados: {lead.empleados_declarados or 'desconocido'}"
    )

    message = client.messages.create(
        model=HAIKU_MODEL,
        max_tokens=150,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = message.content[0].text if message.content else "{}"
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    data = json.loads(match.group(0)) if match else {}

    industria = data.get("industria", "otro").lower().strip()
    if industria not in ("logistica", "tecnologia", "retail", "industrial", "alimentacion", "otro"):
        industria = "otro"

    tamano = data.get("tamano_estimado", "desconocido").lower().strip()
    if tamano not in ("micro", "pequena", "mediana", "grande", "desconocido"):
        tamano = "desconocido"

    prioridad = int(data.get("prioridad", 1))
    prioridad = max(1, min(5, prioridad))

    confianza = data.get("confianza", "baja").lower().strip()
    if confianza not in ("alta", "media", "baja"):
        confianza = "baja"

    motivo = str(data.get("motivo", "Clasificado por Haiku 4.5"))[:120]
    in_tok = message.usage.input_tokens
    out_tok = message.usage.output_tokens

    return industria, tamano, prioridad, confianza, motivo, in_tok, out_tok


def classify_leads(leads: list[RawLead], force_simulation: bool = False) -> Tuple[list[EnrichedLead], CostMetrics]:
    """Enrich and classify a batch of leads, calculating costs."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    enriched: list[EnrichedLead] = []
    total_in = 0
    total_out = 0

    for lead in leads:
        if force_simulation or not api_key:
            ind, sz, prio, conf, mot = rule_based_classify(lead)
            state = "simulado"
        else:
            try:
                ind, sz, prio, conf, mot, in_t, out_t = classify_lead_with_llm(lead, api_key)
                total_in += in_t
                total_out += out_t
                state = "ok"
            except Exception:
                ind, sz, prio, conf, mot = rule_based_classify(lead)
                state = "fallback"

        enriched.append(
            EnrichedLead(
                id=lead.id,
                nombre=lead.nombre,
                web=lead.web,
                email=lead.email,
                telefono=lead.telefono,
                ciudad=lead.ciudad,
                pais=lead.pais,
                categoria_origen=lead.categoria_origen,
                empleados_declarados=lead.empleados_declarados,
                fuente=lead.fuente,
                industria=ind,
                tamano_estimado=sz,
                prioridad=prio,
                confianza=conf,
                motivo=mot,
                estado=state,
            )
        )

    cost_usd = (total_in / 1_000_000 * HAIKU_INPUT_COST_PER_MTOK) + (
        total_out / 1_000_000 * HAIKU_OUTPUT_COST_PER_MTOK
    )
    n = max(len(leads), 1)
    cost_per_lead = cost_usd / n
    cost_100 = cost_per_lead * 100

    metrics = CostMetrics(
        input_tokens=total_in,
        output_tokens=total_out,
        coste_usd=round(cost_usd, 6),
        coste_por_lead_usd=round(cost_per_lead, 6),
        coste_100_leads_usd=round(cost_100, 4),
    )

    return enriched, metrics
