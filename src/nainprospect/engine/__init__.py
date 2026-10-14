"""Engine package exports."""

from src.nainprospect.engine.compliance import is_role_based, sanitize_lead_email, assert_outbound_send_blocked
from src.nainprospect.engine.sourcing import fetch_leads, generate_synthetic_leads
from src.nainprospect.engine.classifier import classify_leads, rule_based_classify
from src.nainprospect.engine.templates import render_template, build_legal_footer, SECTORS
from src.nainprospect.engine.storage import save_run, list_runs, list_leads, get_lead, get_aggregate_metrics

__all__ = [
    "is_role_based",
    "sanitize_lead_email",
    "assert_outbound_send_blocked",
    "fetch_leads",
    "generate_synthetic_leads",
    "classify_leads",
    "rule_based_classify",
    "render_template",
    "build_legal_footer",
    "SECTORS",
    "save_run",
    "list_runs",
    "list_leads",
    "get_lead",
    "get_aggregate_metrics",
]
