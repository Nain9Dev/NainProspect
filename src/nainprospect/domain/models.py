"""Domain models and Pydantic v2 schemas for NainProspect."""

from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

IndustryType = Literal["logistica", "tecnologia", "retail", "industrial", "alimentacion", "otro"]
SizeBandType = Literal["micro", "pequena", "mediana", "grande", "desconocido"]
ConfidenceType = Literal["alta", "media", "baja"]


class RawLead(BaseModel):
    """Raw lead model as sourced before AI classification."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Unique lead identifier")
    nombre: str = Field(description="Company commercial name")
    web: Optional[str] = Field(default="", description="Corporate website URL")
    email: Optional[str] = Field(default=None, description="Role-based corporate email address")
    telefono: Optional[str] = Field(default="", description="Contact phone number")
    ciudad: Optional[str] = Field(default="", description="City of operation")
    pais: str = Field(default="ES", description="Two-letter ISO country code")
    categoria_origen: Optional[str] = Field(default="", description="Category as listed in source")
    empleados_declarados: Optional[int] = Field(default=None, description="Declared headcount if public")
    fuente: str = Field(default="apify", description="Source identifier")


class EnrichedLead(BaseModel):
    """Enriched lead with AI classification and priority scoring."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    nombre: str
    web: Optional[str] = ""
    email: Optional[str] = None
    telefono: Optional[str] = ""
    ciudad: Optional[str] = ""
    pais: str = "ES"
    categoria_origen: Optional[str] = ""
    empleados_declarados: Optional[int] = None
    fuente: str = "apify"

    industria: IndustryType = "otro"
    tamano_estimado: SizeBandType = "desconocido"
    prioridad: int = Field(default=1, ge=1, le=5, description="Outreach priority from 1 (low) to 5 (high)")
    confianza: ConfidenceType = "baja"
    motivo: str = Field(default="", description="Short classification justification")
    estado: str = Field(default="ok", description="Status code ('ok', 'error', 'simulado')")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PipelineRunRequest(BaseModel):
    """Request payload to initiate a prospecting run."""
    query: str = Field(default="empresas de logistica en Madrid", min_length=3, max_length=150)
    limite: int = Field(default=10, ge=1, le=50, description="Maximum number of leads to fetch")
    force_simulation: bool = Field(default=False, description="Force synthetic simulation mode")
    notificar: bool = Field(default=False, description="Send Telegram alert for priority leads")


class CostMetrics(BaseModel):
    """Token usage and dollar cost accounting."""
    input_tokens: int = 0
    output_tokens: int = 0
    coste_usd: float = 0.0
    coste_por_lead_usd: float = 0.0
    coste_100_leads_usd: float = 0.0


class PipelineRunResponse(BaseModel):
    """Output summary of a prospecting execution."""
    run_id: str
    timestamp: str
    query: str
    mode: str
    total_leads: int
    in_target_band: int
    with_email: int
    high_priority_count: int
    coste: CostMetrics
    leads: list[EnrichedLead]


class TemplatePreviewResponse(BaseModel):
    """Rendered email outreach preview with deterministic legal footer."""
    sector: str
    description: str
    subject: str
    recipient: str
    body_html: str
    legal_footer_html: str
    full_html: str


class SystemConfigResponse(BaseModel):
    """System runtime status and active configuration."""
    app_name: str = "NainProspect"
    version: str = "1.0.0"
    mode_description: str
    scraping_mode: str
    classification_mode: str
    telegram_mode: str
    email_dispatch_mode: str = "SIMULADO (LSSI-CE Gate)"
    target_employee_band: str = "50-500 empleados"
    priority_threshold: int = 4
    sender_company: str
    sender_optout: str
