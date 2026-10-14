"""Lead sourcing engine combining Apify Google Places and synthetic generators."""

import os
import uuid
from typing import Optional
from src.nainprospect.domain.models import RawLead
from src.nainprospect.engine.compliance import sanitize_lead_email

SYNTHETIC_BENCHMARK_LEADS: list[dict] = [
    {
        "nombre": "Logistica Meridiano SL",
        "web": "https://meridiano-log.example.com",
        "email": "info@meridiano-log.example.com",
        "telefono": "+34 910 000 001",
        "ciudad": "Madrid",
        "pais": "ES",
        "categoria_origen": "Empresa de transporte y logistica",
        "empleados_declarados": 180,
    },
    {
        "nombre": "Transportes Cordal SA",
        "web": "https://cordal.example.com",
        "email": "contacto@cordal.example.com",
        "telefono": "+34 910 000 002",
        "ciudad": "Madrid",
        "pais": "ES",
        "categoria_origen": "Operador de distribucion",
        "empleados_declarados": 95,
    },
    {
        "nombre": "Almacenes Ribera SL",
        "web": "https://ribera-almacenes.example.com",
        "email": "ventas@ribera-almacenes.example.com",
        "telefono": "+34 910 000 003",
        "ciudad": "Valencia",
        "pais": "ES",
        "categoria_origen": "Almacenaje y cross-docking",
        "empleados_declarados": 240,
    },
    {
        "nombre": "Distribuciones Andes SAS",
        "web": "https://andes-dist.example.com",
        "email": "comercial@andes-dist.example.com",
        "telefono": "+57 1 000 0004",
        "ciudad": "Bogota",
        "pais": "CO",
        "categoria_origen": "Distribuidor regional",
        "empleados_declarados": 310,
    },
    {
        "nombre": "TecnoSur Sistemas SL",
        "web": "https://tecnosur.example.com",
        "email": "info@tecnosur.example.com",
        "telefono": "+34 910 000 005",
        "ciudad": "Sevilla",
        "pais": "ES",
        "categoria_origen": "Desarrollo de software empresarial",
        "empleados_declarados": 120,
    },
    {
        "nombre": "Nube Clara Tecnologia SA",
        "web": "https://nubeclara.example.com",
        "email": "hola@nubeclara.example.com",
        "telefono": "+52 55 0000 0006",
        "ciudad": "Ciudad de Mexico",
        "pais": "MX",
        "categoria_origen": "Servicios Cloud y DevOps",
        "empleados_declarados": 460,
    },
    {
        "nombre": "Retail Pontal SL",
        "web": "https://pontal-retail.example.com",
        "email": "contacto@pontal-retail.example.com",
        "telefono": "+34 910 000 007",
        "ciudad": "Barcelona",
        "pais": "ES",
        "categoria_origen": "Cadena de retail y moda",
        "empleados_declarados": 380,
    },
    {
        "nombre": "Moda Adarve SA",
        "web": "https://adarve.example.com",
        "email": "info@adarve.example.com",
        "telefono": "+34 910 000 008",
        "ciudad": "Zaragoza",
        "pais": "ES",
        "categoria_origen": "Comercio textil y calzado",
        "empleados_declarados": 65,
    },
    {
        "nombre": "Ferreteria Industrial Bego SL",
        "web": "https://bego-ind.example.com",
        "email": "ventas@bego-ind.example.com",
        "telefono": "+34 910 000 009",
        "ciudad": "Bilbao",
        "pais": "ES",
        "categoria_origen": "Suministro y tornilleria industrial",
        "empleados_declarados": 42,
    },
    {
        "nombre": "Grupo Salvia Alimentacion SA",
        "web": "https://salvia-food.example.com",
        "email": "comercial@salvia-food.example.com",
        "telefono": "+34 910 000 010",
        "ciudad": "Murcia",
        "pais": "ES",
        "categoria_origen": "Procesamiento y envasado de alimentos",
        "empleados_declarados": 720,
    },
]


def generate_synthetic_leads(query: str, limit: int = 10) -> list[RawLead]:
    """Generate deterministic synthetic leads for simulation and testing."""
    leads: list[RawLead] = []
    source_pool = SYNTHETIC_BENCHMARK_LEADS

    for i in range(limit):
        base = source_pool[i % len(source_pool)]
        lead_id = f"lead-synth-{i + 1:03d}"
        leads.append(
            RawLead(
                id=lead_id,
                nombre=base["nombre"],
                web=base["web"],
                email=sanitize_lead_email(base["email"]),
                telefono=base["telefono"],
                ciudad=base["ciudad"],
                pais=base["pais"],
                categoria_origen=base["categoria_origen"],
                empleados_declarados=base["empleados_declarados"],
                fuente="synthetic-generator",
            )
        )
    return leads


def fetch_leads(query: str, limit: int = 10, force_simulation: bool = False) -> list[RawLead]:
    """Fetch leads from Apify actor or fallback to synthetic simulation."""
    apify_token = os.getenv("APIFY_API_TOKEN", "").strip()

    if force_simulation or not apify_token:
        return generate_synthetic_leads(query=query, limit=limit)

    try:
        from apify_client import ApifyClient
        client = ApifyClient(apify_token)
        actor_id = os.getenv("APIFY_ACTOR_ID", "compass/crawler-google-places")

        run_input = {
            "searchStringsArray": [query],
            "maxCrawledPlacesPerSearch": limit,
            "language": "es",
        }
        run = client.actor(actor_id).call(run_input=run_input, timeout_secs=120)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        leads: list[RawLead] = []
        for idx, item in enumerate(items[:limit]):
            raw_email = item.get("email") or ""
            lead = RawLead(
                id=f"apify-{idx+1}-{uuid.uuid4().hex[:6]}",
                nombre=item.get("title") or item.get("name") or "Empresa Desconocida",
                web=item.get("website") or "",
                email=sanitize_lead_email(raw_email),
                telefono=item.get("phone") or "",
                ciudad=item.get("city") or "Espana",
                pais="ES",
                categoria_origen=item.get("categoryName") or query,
                empleados_declarados=None,
                fuente="apify-places",
            )
            leads.append(lead)
        return leads
    except Exception:
        # Fallback to simulation if network or credentials fail
        return generate_synthetic_leads(query=query, limit=limit)
