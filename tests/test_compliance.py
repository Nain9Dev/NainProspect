"""Unit tests for compliance guardrails and GDPR/LSSI-CE rules."""

import pytest
from src.nainprospect.engine.compliance import (
    is_role_based,
    sanitize_lead_email,
    assert_outbound_send_blocked,
)


def test_role_based_emails_are_allowed():
    """Verify that generic corporate mailbox prefixes are accepted."""
    assert is_role_based("info@empresa.com") is True
    assert is_role_based("contacto@logistica-nain.es") is True
    assert is_role_based("ventas@tech-corp.com") is True
    assert is_role_based("hola@nubeclara.example.com") is True
    assert is_role_based("soporte@domain.org") is True
    assert is_role_based("marketing@brand.co") is True


def test_personal_named_emails_are_strictly_rejected():
    """Verify that named individual emails are rejected to protect GDPR personal data."""
    assert is_role_based("antonio.perez@empresa.com") is False
    assert is_role_based("marta.lopez@corporacion.es") is False
    assert is_role_based("john.doe@tech.com") is False
    assert is_role_based("ceo@domain.com") is False
    assert is_role_based("director.comercial@agency.es") is False
    assert is_role_based("") is False
    assert is_role_based(None) is False
    assert is_role_based("invalid-email-format") is False


def test_sanitize_lead_email_strips_named_addresses():
    """Sanitize lead email returns cleaned string or None."""
    assert sanitize_lead_email("  INFO@EMPRESA.COM  ") == "info@empresa.com"
    assert sanitize_lead_email("carlos.sanchez@empresa.com") is None
    assert sanitize_lead_email(None) is None


def test_outbound_send_compliance_gate_raises_error():
    """Verify that automated cold email transmission is locked (BR-02)."""
    with pytest.raises(PermissionError) as exc_info:
        assert_outbound_send_blocked()

    assert "compliance gate" in str(exc_info.value).lower()
    assert "lssi-ce" in str(exc_info.value).lower()
