"""Unit tests for classification and priority scoring rules."""

from src.nainprospect.domain.models import RawLead
from src.nainprospect.engine.classifier import rule_based_classify, classify_leads


def test_rule_based_classifier_target_medium_company():
    """Verify medium company (50-500) with corporate email receives priority 5."""
    lead = RawLead(
        id="test-001",
        nombre="Logistica Central SL",
        web="https://logcentral.example.com",
        email="info@logcentral.example.com",
        ciudad="Madrid",
        categoria_origen="Empresa de transporte y logistica",
        empleados_declarados=150,
    )

    ind, sz, prio, conf, _ = rule_based_classify(lead)
    assert ind == "logistica"
    assert sz == "mediana"
    assert prio == 5
    assert conf == "alta"


def test_rule_based_classifier_small_company():
    """Verify company under 50 employees receives priority 2."""
    lead = RawLead(
        id="test-002",
        nombre="Taller Mecanico Express",
        email="contacto@taller.example.com",
        categoria_origen="Taller y mecanica industrial",
        empleados_declarados=15,
    )

    ind, sz, prio, _, _ = rule_based_classify(lead)
    assert ind == "industrial"
    assert sz == "pequena"
    assert prio == 2


def test_classify_batch_simulation_cost_accounting():
    """Verify batch classification metrics and zero cost in simulation."""
    leads = [
        RawLead(id="1", nombre="A SL", categoria_origen="Software", empleados_declarados=100),
        RawLead(id="2", nombre="B SA", categoria_origen="Transportes", empleados_declarados=250),
    ]

    enriched, metrics = classify_leads(leads, force_simulation=True)
    assert len(enriched) == 2
    assert enriched[0].tamano_estimado == "mediana"
    assert metrics.coste_usd == 0.0
    assert metrics.input_tokens == 0
