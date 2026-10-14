"""Unit tests for template generation and deterministic legal footers."""

from src.nainprospect.engine.templates import build_legal_footer, render_template, SECTORS


def test_legal_footer_contains_statutory_requirements():
    """Verify LSSI-CE Article 21 and GDPR 6.1.f required elements."""
    footer = build_legal_footer(
        company_name="Test Company SL",
        legal_id="B12345678",
        address="Paseo de la Castellana 1, Madrid",
        optout_email="bajas@testcompany.com",
    )

    assert "Test Company SL" in footer
    assert "B12345678" in footer
    assert "Paseo de la Castellana 1, Madrid" in footer
    assert "bajas@testcompany.com" in footer
    assert "articulo 6.1.f del RGPD" in footer
    assert "interes legitimo" in footer


def test_render_template_substitutions():
    """Verify placeholder replacement in template rendering."""
    preview = render_template(
        sector="logistica",
        company="Transportes del Norte SA",
        city="Santander",
        recipient="info@transportesnorte.com",
    )

    assert preview.sector == "logistica"
    assert preview.recipient == "info@transportesnorte.com"
    assert "Transportes del Norte SA" in preview.body_html
    assert "Santander" in preview.body_html
    assert "{{NOMBRE_EMPRESA}}" not in preview.body_html
    assert "{{CIUDAD}}" not in preview.body_html
    assert "PUBLICIDAD / COMUNICACION COMERCIAL" in preview.full_html


def test_unknown_sector_falls_back_gracefully():
    """Verify fallback to technology when an unknown sector is requested."""
    preview = render_template(sector="aeronautica_espacial")
    assert preview.sector == "tecnologia"
