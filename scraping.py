"""Lead sourcing from public company data.

Two sources are supported:

* Apify Google Maps actor, for public business listings.
* The company's own website, to recover a generic contact address.

LinkedIn is deliberately not implemented: scraping it breaches their terms of
service and the profiles are personal data of individuals rather than company
data. See README.md, section "Limites legales".

Only role-based addresses (info@, contacto@, ventas@...) are kept. Addresses
that look like a named person are discarded on purpose, so the dataset stays
at company level.
"""

import csv
import re
import time

import requests

import config

REQUEST_TIMEOUT_SECONDS = 10
MAX_PAGES_PER_SITE = 3

# Role-based prefixes we accept. Anything else is treated as a named person
# and dropped, which keeps the dataset out of the riskiest GDPR territory.
ROLE_BASED_PREFIXES = {
    "info", "contacto", "contact", "hola", "hello", "ventas", "sales",
    "comercial", "administracion", "admin", "soporte", "support", "oficina",
    "office", "general", "atencionalcliente", "clientes", "marketing",
}

EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

CONTACT_PATHS = ["", "/contacto", "/contact", "/es/contacto", "/quienes-somos"]

LEAD_FIELDS = [
    "nombre",
    "web",
    "email",
    "telefono",
    "ciudad",
    "pais",
    "categoria_origen",
    "empleados_declarados",
    "fuente",
]

# Synthetic dataset used when APIFY_API_TOKEN is absent. Fictional companies
# and example.com domains on purpose: no real personal data in tests.
LEADS_SIMULADOS = [
    {"nombre": "Logistica Meridiano SL", "web": "https://meridiano-log.example.com",
     "email": "info@meridiano-log.example.com", "telefono": "+34 910 000 001",
     "ciudad": "Madrid", "pais": "ES", "categoria_origen": "Empresa de transporte",
     "empleados_declarados": 180},
    {"nombre": "Transportes Cordal SA", "web": "https://cordal.example.com",
     "email": "contacto@cordal.example.com", "telefono": "+34 910 000 002",
     "ciudad": "Madrid", "pais": "ES", "categoria_origen": "Empresa de logistica",
     "empleados_declarados": 95},
    {"nombre": "Almacenes Ribera SL", "web": "https://ribera-almacenes.example.com",
     "email": "ventas@ribera-almacenes.example.com", "telefono": "+34 910 000 003",
     "ciudad": "Valencia", "pais": "ES", "categoria_origen": "Almacen",
     "empleados_declarados": 240},
    {"nombre": "Distribuciones Andes SAS", "web": "https://andes-dist.example.com",
     "email": "comercial@andes-dist.example.com", "telefono": "+57 1 000 0004",
     "ciudad": "Bogota", "pais": "CO", "categoria_origen": "Distribuidor",
     "empleados_declarados": 310},
    {"nombre": "TecnoSur Sistemas SL", "web": "https://tecnosur.example.com",
     "email": "info@tecnosur.example.com", "telefono": "+34 910 000 005",
     "ciudad": "Sevilla", "pais": "ES", "categoria_origen": "Software",
     "empleados_declarados": 120},
    {"nombre": "Nube Clara Tecnologia SA", "web": "https://nubeclara.example.com",
     "email": "hola@nubeclara.example.com", "telefono": "+52 55 0000 0006",
     "ciudad": "Ciudad de Mexico", "pais": "MX", "categoria_origen": "Servicios IT",
     "empleados_declarados": 460},
    {"nombre": "Retail Pontal SL", "web": "https://pontal-retail.example.com",
     "email": "contacto@pontal-retail.example.com", "telefono": "+34 910 000 007",
     "ciudad": "Barcelona", "pais": "ES", "categoria_origen": "Cadena de tiendas",
     "empleados_declarados": 380},
    {"nombre": "Moda Adarve SA", "web": "https://adarve.example.com",
     "email": "info@adarve.example.com", "telefono": "+34 910 000 008",
     "ciudad": "Zaragoza", "pais": "ES", "categoria_origen": "Comercio textil",
     "empleados_declarados": 65},
    {"nombre": "Ferreteria Industrial Bego SL", "web": "https://bego-ind.example.com",
     "email": "ventas@bego-ind.example.com", "telefono": "+34 910 000 009",
     "ciudad": "Bilbao", "pais": "ES", "categoria_origen": "Suministro industrial",
     "empleados_declarados": 42},
    {"nombre": "Grupo Salvia Alimentacion SA", "web": "https://salvia-food.example.com",
     "email": "comercial@salvia-food.example.com", "telefono": "+34 910 000 010",
     "ciudad": "Murcia", "pais": "ES", "categoria_origen": "Alimentacion",
     "empleados_declarados": 720},
]


def is_role_based(email):
    """Return True when the address is a generic company mailbox."""
    if not email or "@" not in email:
        return False
    prefix = email.split("@", 1)[0].lower()
    prefix = re.sub(r"[^a-z]", "", prefix)
    return prefix in ROLE_BASED_PREFIXES


def extract_role_email(html, domain_hint=None):
    """Return the first role-based address found in an HTML page."""
    for candidate in EMAIL_PATTERN.findall(html or ""):
        candidate = candidate.lower().rstrip(".")
        if candidate.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            continue
        if not is_role_based(candidate):
            continue
        if domain_hint and domain_hint not in candidate:
            continue
        return candidate
    return None


def enrich_from_website(lead):
    """Try to recover a generic contact address from the company website.

    Never raises: a lead without email is still a valid lead.
    """
    web = (lead.get("web") or "").strip()
    if not web or lead.get("email"):
        return lead

    domain = re.sub(r"^https?://(www\.)?", "", web).split("/")[0].lower()
    session = requests.Session()
    session.headers.update({"User-Agent": "prospeccion-b2b/1.0 (+contacto)"})

    for path in CONTACT_PATHS[:MAX_PAGES_PER_SITE]:
        try:
            response = session.get(
                web.rstrip("/") + path, timeout=REQUEST_TIMEOUT_SECONDS
            )
        except requests.RequestException:
            continue
        if response.status_code != 200:
            continue
        found = extract_role_email(response.text, domain_hint=domain)
        if found:
            lead["email"] = found
            return lead
        time.sleep(0.5)

    return lead


def _map_apify_item(item):
    """Translate one Apify Google Maps item into our lead shape."""
    return {
        "nombre": item.get("title") or item.get("name") or "",
        "web": item.get("website") or "",
        "email": "",
        "telefono": item.get("phone") or "",
        "ciudad": item.get("city") or "",
        "pais": item.get("countryCode") or "",
        "categoria_origen": item.get("categoryName") or "",
        # Google Maps does not expose headcount. Left empty on purpose and
        # estimated later by the classifier, flagged as low confidence.
        "empleados_declarados": "",
        "fuente": "google_maps_apify",
    }


def scrape_apify(query, limit):
    """Run the Apify Google Maps actor and return raw leads."""
    from apify_client import ApifyClient

    client = ApifyClient(config.APIFY_API_TOKEN)
    run_input = {
        "searchStringsArray": [query],
        "maxCrawledPlacesPerSearch": limit,
        "language": "es",
        "skipClosedPlaces": True,
    }
    run = client.actor(config.APIFY_ACTOR_ID).call(run_input=run_input)
    dataset_id = run.get("defaultDatasetId")
    if not dataset_id:
        return []

    leads = []
    for item in client.dataset(dataset_id).iterate_items():
        leads.append(_map_apify_item(item))
        if len(leads) >= limit:
            break
    return leads


def buscar_leads(query, limit=10):
    """Return up to `limit` leads for a search query.

    Falls back to the synthetic dataset when no Apify token is configured, so
    the pipeline is always runnable end to end without spending money.
    """
    if config.scraping_is_simulated():
        leads = []
        for row in LEADS_SIMULADOS[:limit]:
            lead = dict(row)
            lead["fuente"] = "simulado"
            leads.append(lead)
        return leads

    leads = scrape_apify(query, limit)
    enriched = []
    for lead in leads:
        enriched.append(enrich_from_website(lead))
    return enriched


def guardar_csv(leads, path=None):
    """Write leads to CSV and return the path used."""
    config.ensure_directories()
    destination = path or config.LEADS_RAW_CSV
    with open(destination, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEAD_FIELDS)
        writer.writeheader()
        for lead in leads:
            writer.writerow({field: lead.get(field, "") for field in LEAD_FIELDS})
    return destination


if __name__ == "__main__":
    import sys

    consulta = sys.argv[1] if len(sys.argv) > 1 else "empresas de logistica en Madrid"
    tope = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print("Modo: " + config.describe_mode())
    resultados = buscar_leads(consulta, tope)
    ruta = guardar_csv(resultados)
    print("Leads obtenidos: " + str(len(resultados)))
    print("Guardado en: " + str(ruta))
