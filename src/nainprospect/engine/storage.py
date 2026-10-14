"""Thread-safe storage manager for pipeline runs and leads."""

import threading
from typing import Optional
from src.nainprospect.domain.models import EnrichedLead, PipelineRunResponse, CostMetrics
from src.nainprospect.engine.sourcing import generate_synthetic_leads
from src.nainprospect.engine.classifier import classify_leads

_LOCK = threading.Lock()
_PIPELINE_RUNS: list[PipelineRunResponse] = []
_ALL_LEADS: dict[str, EnrichedLead] = {}


def _init_seed_data_if_empty() -> None:
    """Pre-seed with realistic benchmark leads for demo and UI inspection."""
    if _ALL_LEADS:
        return

    raw = generate_synthetic_leads(query="empresas de logistica en Madrid", limit=10)
    enriched, metrics = classify_leads(raw, force_simulation=True)

    for l in enriched:
        _ALL_LEADS[l.id] = l

    in_target = sum(1 for l in enriched if l.tamano_estimado == "mediana")
    with_email = sum(1 for l in enriched if l.email)
    high_prio = sum(1 for l in enriched if l.prioridad >= 4)

    run = PipelineRunResponse(
        run_id="run-init-seed",
        timestamp="2026-10-14T20:00:00Z",
        query="empresas de logistica en Madrid",
        mode="SIMULADO (Seed)",
        total_leads=len(enriched),
        in_target_band=in_target,
        with_email=with_email,
        high_priority_count=high_prio,
        coste=metrics,
        leads=enriched,
    )
    _PIPELINE_RUNS.append(run)


def save_run(run: PipelineRunResponse) -> None:
    """Save a completed pipeline execution."""
    with _LOCK:
        _PIPELINE_RUNS.insert(0, run)
        for lead in run.leads:
            _ALL_LEADS[lead.id] = lead


def list_runs() -> list[PipelineRunResponse]:
    """Retrieve all recorded pipeline executions."""
    with _LOCK:
        _init_seed_data_if_empty()
        return list(_PIPELINE_RUNS)


def list_leads(
    sector: Optional[str] = None,
    min_priority: Optional[int] = None,
    has_email: Optional[bool] = None,
) -> list[EnrichedLead]:
    """Filter leads based on criteria."""
    with _LOCK:
        _init_seed_data_if_empty()
        leads = list(_ALL_LEADS.values())

    if sector:
        leads = [l for l in leads if l.industria.lower() == sector.lower()]
    if min_priority is not None:
        leads = [l for l in leads if l.prioridad >= min_priority]
    if has_email is True:
        leads = [l for l in leads if l.email]
    elif has_email is False:
        leads = [l for l in leads if not l.email]

    # Sort descending by priority, then name
    leads.sort(key=lambda l: (-l.prioridad, l.nombre))
    return leads


def get_lead(lead_id: str) -> Optional[EnrichedLead]:
    """Retrieve a single lead by ID."""
    with _LOCK:
        _init_seed_data_if_empty()
        return _ALL_LEADS.get(lead_id)


def get_aggregate_metrics() -> dict:
    """Compute aggregate counts across all known leads."""
    with _LOCK:
        _init_seed_data_if_empty()
        leads = list(_ALL_LEADS.values())

    return {
        "total_leads": len(leads),
        "in_target_band": sum(1 for l in leads if l.tamano_estimado == "mediana"),
        "with_email": sum(1 for l in leads if l.email),
        "priority_5_count": sum(1 for l in leads if l.prioridad == 5),
        "priority_4_count": sum(1 for l in leads if l.prioridad == 4),
        "low_priority_count": sum(1 for l in leads if l.prioridad <= 2),
        "total_runs": len(_PIPELINE_RUNS),
    }
