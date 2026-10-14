"""Integration tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from src.nainprospect.main import app

client = TestClient(app)


def test_health_and_readiness_endpoints():
    """Verify liveness and readiness probes."""
    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    res_ready = client.get("/health/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "ready"


def test_get_system_config():
    """Verify system config endpoint."""
    res = client.get("/api/config")
    assert res.status_code == 200
    data = res.json()
    assert data["app_name"] == "NainProspect"
    assert "email_dispatch_mode" in data
    assert "target_employee_band" in data


def test_trigger_pipeline_run_and_list_leads():
    """Verify pipeline execution and subsequent lead retrieval."""
    payload = {
        "query": "empresas de logistica en Valencia",
        "limite": 5,
        "force_simulation": True,
        "notificar": False,
    }
    res = client.post("/api/pipeline/run", json=payload)
    assert res.status_code == 200
    run_data = res.json()
    assert run_data["total_leads"] == 5
    assert len(run_data["leads"]) == 5
    assert run_data["mode"] == "SIMULADO"

    # Verify leads listing
    res_leads = client.get("/api/leads")
    assert res_leads.status_code == 200
    leads = res_leads.json()
    assert len(leads) >= 5


def test_preview_template_endpoint():
    """Verify template preview endpoint."""
    res = client.get("/api/templates/logistica/preview")
    assert res.status_code == 200
    data = res.json()
    assert data["sector"] == "logistica"
    assert "body_html" in data
    assert "legal_footer_html" in data


def test_compliance_verify_send_is_forbidden():
    """Verify outbound send gate returns 403 Forbidden with legal basis."""
    res = client.post("/api/compliance/verify-send")
    assert res.status_code == 403
    error_detail = res.json()["detail"]
    assert error_detail["error"] == "COMPLIANCE_GATE_ACTIVE"
    assert "LSSI-CE" in error_detail["legal_basis"]
