"""FastAPI REST routes for NainProspect Gateway."""

import os
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from src.nainprospect.domain.models import (
    EnrichedLead,
    PipelineRunRequest,
    PipelineRunResponse,
    TemplatePreviewResponse,
    SystemConfigResponse,
)
from src.nainprospect.engine.compliance import assert_outbound_send_blocked
from src.nainprospect.engine.sourcing import fetch_leads
from src.nainprospect.engine.classifier import classify_leads
from src.nainprospect.engine.templates import render_template, SECTORS
from src.nainprospect.engine.storage import (
    save_run,
    list_runs,
    list_leads,
    get_lead,
    get_aggregate_metrics,
)

router = APIRouter(prefix="/api", tags=["Prospecting Gateway"])


@router.get("/config", response_model=SystemConfigResponse)
def get_system_config() -> SystemConfigResponse:
    """Retrieve system operating mode, active legal constraints, and configuration."""
    has_apify = bool(os.getenv("APIFY_API_TOKEN", "").strip())
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY", "").strip())
    has_telegram = bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))

    scraping_mode = "APIFY (Google Places)" if has_apify else "SIMULADO (Synthetic fixtures)"
    class_mode = "ANTHROPIC (Claude Haiku 4.5)" if has_anthropic else "SIMULADO (Deterministic Heuristic)"
    tg_mode = "ACTIVO (Bot Telegram)" if has_telegram else "CONSOLA / DESACTIVADO"

    mode_desc = f"scraping={'REAL' if has_apify else 'SIMULADO'} | clasificacion={'REAL' if has_anthropic else 'SIMULADO'} | email=BLOQUEADO_LSSI"

    return SystemConfigResponse(
        mode_description=mode_desc,
        scraping_mode=scraping_mode,
        classification_mode=class_mode,
        telegram_mode=tg_mode,
        email_dispatch_mode="SIMULADO (Bloqueo LSSI-CE Art. 21)",
        target_employee_band="50-500 empleados",
        priority_threshold=4,
        sender_company=os.getenv("SENDER_COMPANY_NAME", "NainDev Software Architecture"),
        sender_optout=os.getenv("SENDER_OPTOUT_EMAIL", "bajas@naindev.com"),
    )


@router.post("/pipeline/run", response_model=PipelineRunResponse)
def trigger_pipeline_run(request: PipelineRunRequest) -> PipelineRunResponse:
    """Execute a prospecting run: fetch/generate leads, classify with AI, and score."""
    raw_leads = fetch_leads(
        query=request.query,
        limit=request.limite,
        force_simulation=request.force_simulation,
    )

    enriched_leads, cost_metrics = classify_leads(
        leads=raw_leads,
        force_simulation=request.force_simulation,
    )

    in_target = sum(1 for l in enriched_leads if l.tamano_estimado == "mediana")
    with_email = sum(1 for l in enriched_leads if l.email)
    high_prio = sum(1 for l in enriched_leads if l.prioridad >= 4)

    run_id = f"run-{uuid.uuid4().hex[:8]}"
    mode_label = "SIMULADO" if request.force_simulation or not os.getenv("ANTHROPIC_API_KEY") else "REAL (Claude Haiku 4.5)"

    response = PipelineRunResponse(
        run_id=run_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        query=request.query,
        mode=mode_label,
        total_leads=len(enriched_leads),
        in_target_band=in_target,
        with_email=with_email,
        high_priority_count=high_prio,
        coste=cost_metrics,
        leads=enriched_leads,
    )

    save_run(response)
    return response


@router.get("/pipeline/runs", response_model=list[PipelineRunResponse])
def get_pipeline_runs() -> list[PipelineRunResponse]:
    """Retrieve all recorded pipeline executions."""
    return list_runs()


@router.get("/leads", response_model=list[EnrichedLead])
def get_leads(
    sector: Optional[str] = Query(None, description="Filter by industry (e.g. logistica, tecnologia, retail)"),
    min_priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by minimum priority score (1-5)"),
    has_email: Optional[bool] = Query(None, description="Filter by presence of valid role-based email"),
) -> list[EnrichedLead]:
    """List and filter enriched leads."""
    return list_leads(sector=sector, min_priority=min_priority, has_email=has_email)


@router.get("/leads/{lead_id}", response_model=EnrichedLead)
def get_single_lead(lead_id: str) -> EnrichedLead:
    """Retrieve details for a specific lead."""
    lead = get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lead '{lead_id}' not found")
    return lead


@router.get("/templates")
def list_templates() -> dict[str, str]:
    """List available template sectors and target descriptions."""
    return SECTORS


@router.get("/templates/{sector}/preview", response_model=TemplatePreviewResponse)
def preview_template(
    sector: str,
    lead_id: Optional[str] = Query(None, description="Optional lead ID to populate placeholders with"),
) -> TemplatePreviewResponse:
    """Preview rendered email template with live placeholders and legal footer."""
    company = "Empresa Ejemplo SL"
    city = "Madrid"
    recipient = "contacto@ejemplo.com"

    if lead_id:
        lead = get_lead(lead_id)
        if lead:
            company = lead.nombre
            city = lead.ciudad or "Madrid"
            recipient = lead.email or "contacto@ejemplo.com"

    return render_template(
        sector=sector,
        company=company,
        city=city,
        recipient=recipient,
    )


@router.get("/metrics")
def get_metrics() -> dict:
    """Get aggregate lead pipeline metrics and statistics."""
    return get_aggregate_metrics()


@router.post("/compliance/verify-send")
def verify_outbound_dispatch() -> None:
    """Enforce the compliance send gate (BR-02). Demonstrates technical lock."""
    try:
        assert_outbound_send_blocked()
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "COMPLIANCE_GATE_ACTIVE",
                "message": str(exc),
                "legal_basis": "Spanish LSSI-CE Article 21 & GDPR 6.1.f",
                "status": "Outreach dispatch locked in simulation mode",
            },
        )
