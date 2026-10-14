"""Template rendering engine with deterministic LSSI-CE Article 21 legal footer."""

import os
from typing import Optional
from src.nainprospect.domain.models import TemplatePreviewResponse

SECTORS = {
    "retail": "Cadenas de tienda y comercio minorista",
    "tecnologia": "Empresas de software y servicios IT",
    "logistica": "Operadores logisticos y transporte",
}

DEFAULT_BODIES = {
    "retail": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>\n"
        "<p>Trabajo con cadenas de tienda en {{CIUDAD}} que gestionan surtido y "
        "stock en varios puntos de venta a la vez.</p>\n"
        "<p>Si os encaja, podemos ensenaros en quince minutos como reducir el "
        "trabajo manual de consolidar esa informacion.</p>"
    ),
    "tecnologia": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>\n"
        "<p>Trabajo con empresas de software en {{CIUDAD}} que necesitan sostener "
        "su ritmo de entrega sin ampliar el equipo.</p>\n"
        "<p>Si os resulta util, podemos ensenaros en quince minutos donde suele "
        "estar el cuello de botella.</p>"
    ),
    "logistica": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>\n"
        "<p>Trabajo con operadores logisticos en {{CIUDAD}} que coordinan rutas y "
        "documentacion con procesos todavia manuales.</p>\n"
        "<p>Si os interesa, podemos ensenaros en quince minutos como automatizar "
        "esa parte.</p>"
    ),
}

SUBJECT_LINES = {
    "retail": "Eficiencia en consolidacion de inventario para {{NOMBRE_EMPRESA}}",
    "tecnologia": "Cuello de botella en entrega continua para {{NOMBRE_EMPRESA}}",
    "logistica": "Automatizacion de rutas y partes de transporte - {{NOMBRE_EMPRESA}}",
}


def build_legal_footer(
    company_name: Optional[str] = None,
    legal_id: Optional[str] = None,
    address: Optional[str] = None,
    optout_email: Optional[str] = None,
) -> str:
    """Build the immutable LSSI-CE Article 21 and GDPR 6.1.f legal footer."""
    company = company_name or os.getenv("SENDER_COMPANY_NAME") or "NainDev Software Architecture"
    nif_cif = legal_id or os.getenv("SENDER_LEGAL_ID") or "ES-B99999999"
    addr = address or os.getenv("SENDER_ADDRESS") or "Calle Principal 10, 28001 Madrid, Espana"
    optout = optout_email or os.getenv("SENDER_OPTOUT_EMAIL") or "bajas@naindev.com"

    return (
        '<hr style="border:none;border-top:1px solid #334155;margin:24px 0">\n'
        '<p style="font-size:12px;color:#94a3b8;line-height:1.5">\n'
        f"Comunicacion comercial enviada por <strong>{company}</strong>, "
        f"CIF/NIF {nif_cif}, con domicilio en {addr}. Hemos obtenido tu direccion de contacto "
        "profesional de fuentes de acceso publico y te escribimos amparados en "
        "el interes legitimo previsto en el articulo 6.1.f del RGPD.<br>\n"
        f'Puedes oponerte a este tratamiento y causar baja inmediata escribiendo a '
        f'<a href="mailto:{optout}" style="color:#38bdf8">{optout}</a>. '
        "Tu solicitud sera tramitada sin dilacion de forma irrevocable."
        "</p>"
    )


def render_template(
    sector: str,
    company: str = "Empresa Ejemplo SL",
    city: str = "Madrid",
    recipient: str = "contacto@ejemplo.com",
) -> TemplatePreviewResponse:
    """Render a full email HTML preview with substitutions."""
    sec = sector.lower().strip()
    if sec not in SECTORS:
        sec = "tecnologia"

    body_template = DEFAULT_BODIES[sec]
    subject_template = SUBJECT_LINES[sec]

    body_html = (
        body_template
        .replace("{{NOMBRE_EMPRESA}}", company)
        .replace("{{CIUDAD}}", city)
    )

    subject = subject_template.replace("{{NOMBRE_EMPRESA}}", company)
    footer_html = build_legal_footer()

    full_html = (
        "<!DOCTYPE html>\n"
        '<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{subject}</title>\n</head>\n"
        '<body style="margin:0;padding:20px;background:#0f172a;font-family:system-ui,-apple-system,sans-serif;color:#f8fafc">\n'
        '<div style="max-width:620px;margin:0 auto;background:#1e293b;border:1px solid #334155;border-radius:12px;padding:32px">\n'
        '<p style="font-size:11px;color:#38bdf8;text-transform:uppercase;letter-spacing:1px;margin:0 0 16px;font-weight:bold">'
        'PUBLICIDAD / COMUNICACION COMERCIAL'
        "</p>\n"
        f"{body_html}\n"
        f"{footer_html}\n"
        "</div>\n</body>\n</html>"
    )

    return TemplatePreviewResponse(
        sector=sec,
        description=SECTORS[sec],
        subject=subject,
        recipient=recipient,
        body_html=body_html,
        legal_footer_html=footer_html,
        full_html=full_html,
    )
