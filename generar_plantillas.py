"""HTML email template generation.

The body copy is written by Claude Haiku 4.5. The legal footer is NOT: it is
built deterministically in Python from the SENDER_* settings, because article
21 of the Spanish LSSI-CE requires the message to be identifiable as a
commercial communication, to identify the sender, and to offer a working
opt-out. Those three things must never depend on what a model happens to
generate.

Placeholders left for the caller to replace:
  {{NOMBRE_EMPRESA}}  {{CIUDAD}}  {{INDUSTRIA}}  {{EMAIL_LEAD}}
"""

import config

SECTORS = {
    "retail": "cadenas de tienda y comercio minorista",
    "tecnologia": "empresas de software y servicios IT",
    "logistica": "operadores logisticos y de transporte",
}

MAX_OUTPUT_TOKENS = 700

BODY_PROMPT = (
    "Write the HTML body of a cold B2B outreach email in Spanish, aimed at "
    "{descripcion}. Constraints: under 120 words, no exaggerated claims, no "
    "invented figures, no emoji, plain professional tone. Use only <p>, "
    "<strong> and <ul>/<li> tags. Include the placeholders {{{{NOMBRE_EMPRESA}}}} "
    "and {{{{CIUDAD}}}} naturally in the text. Do not write a greeting header, a "
    "signature, a subject line or any footer. Return only the HTML fragment."
)

FALLBACK_BODIES = {
    "retail": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>"
        "<p>Trabajo con cadenas de tienda en {{CIUDAD}} que gestionan surtido y "
        "stock en varios puntos de venta a la vez.</p>"
        "<p>Si os encaja, puedo ensenaros en quince minutos como reducir el "
        "trabajo manual de consolidar esa informacion.</p>"
    ),
    "tecnologia": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>"
        "<p>Trabajo con empresas de software en {{CIUDAD}} que necesitan sostener "
        "su ritmo de entrega sin ampliar el equipo.</p>"
        "<p>Si os resulta util, puedo ensenaros en quince minutos donde suele "
        "estar el cuello de botella.</p>"
    ),
    "logistica": (
        "<p>Hola, equipo de <strong>{{NOMBRE_EMPRESA}}</strong>:</p>"
        "<p>Trabajo con operadores logisticos en {{CIUDAD}} que coordinan rutas y "
        "documentacion con procesos todavia manuales.</p>"
        "<p>Si os interesa, puedo ensenaros en quince minutos como automatizar "
        "esa parte.</p>"
    ),
}


def build_legal_footer():
    """Build the LSSI-CE compliant footer from configuration."""
    company = config.SENDER_COMPANY_NAME or "[PENDIENTE: SENDER_COMPANY_NAME]"
    legal_id = config.SENDER_LEGAL_ID or "[PENDIENTE: SENDER_LEGAL_ID]"
    address = config.SENDER_ADDRESS or "[PENDIENTE: SENDER_ADDRESS]"
    optout = config.SENDER_OPTOUT_EMAIL or "[PENDIENTE: SENDER_OPTOUT_EMAIL]"

    return (
        '<hr style="border:none;border-top:1px solid #e0e0e0;margin:24px 0">'
        '<p style="font-size:12px;color:#666;line-height:1.5">'
        "Comunicacion comercial enviada por <strong>{company}</strong>, "
        "{legal_id}, {address}. Hemos obtenido tu direccion de contacto "
        "profesional de fuentes de acceso publico y te escribimos amparados en "
        "el interes legitimo previsto en el articulo 6.1.f del RGPD. "
        'Puedes oponerte a este tratamiento y dejar de recibir estos mensajes '
        'escribiendo a <a href="mailto:{optout}">{optout}</a>. '
        "Trataremos tu solicitud de forma inmediata."
        "</p>"
    ).format(company=company, legal_id=legal_id, address=address, optout=optout)


def wrap_html(sector, body_html):
    """Wrap a body fragment in the full HTML document."""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>Contacto comercial - {sector}</title>\n</head>\n"
        '<body style="margin:0;padding:0;background:#f5f5f5">\n'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        'style="background:#f5f5f5;padding:24px 0">\n<tr><td align="center">\n'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        'style="max-width:600px;background:#ffffff;border-radius:8px;'
        'padding:32px;font-family:Arial,Helvetica,sans-serif;font-size:15px;'
        'line-height:1.6;color:#222">\n<tr><td>\n'
        '<p style="font-size:11px;color:#888;text-transform:uppercase;'
        'letter-spacing:.5px;margin:0 0 16px">Publicidad</p>\n'
        "{body}\n{footer}\n"
        "</td></tr>\n</table>\n</td></tr>\n</table>\n</body>\n</html>\n"
    ).format(sector=sector, body=body_html, footer=build_legal_footer())


def generate_body(client, sector):
    """Ask Haiku for the body copy of one sector template."""
    message = client.messages.create(
        model=config.HAIKU_MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{
            "role": "user",
            "content": BODY_PROMPT.format(descripcion=SECTORS[sector]),
        }],
    )
    return message.content[0].text.strip()


def generar_plantillas(verbose=True):
    """Write one HTML template per sector and return the paths."""
    config.ensure_directories()
    client = None
    if not config.classification_is_simulated():
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    written = []
    for sector in SECTORS:
        if client is None:
            body = FALLBACK_BODIES[sector]
        else:
            try:
                body = generate_body(client, sector)
            except Exception as error:  # noqa: BLE001 - fall back, never block
                print("  Fallo generando {0}: {1}. Uso plantilla base.".format(
                    sector, type(error).__name__))
                body = FALLBACK_BODIES[sector]

        path = config.TEMPLATES_DIR / "{0}.html".format(sector)
        path.write_text(wrap_html(sector, body), encoding="utf-8")
        written.append(path)
        if verbose:
            print("Plantilla escrita: " + str(path))

    return written


if __name__ == "__main__":
    print("Modo: " + config.describe_mode())
    generar_plantillas()
