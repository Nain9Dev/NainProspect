"""Telegram notifications.

Falls back to console output when the bot is not configured, so the pipeline
never fails because of a missing notification channel.
"""

import requests

import config

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
REQUEST_TIMEOUT_SECONDS = 15
MAX_MESSAGE_LENGTH = 4000


def build_summary(rows):
    """Build the notification text for the high-priority leads."""
    priority_leads = [
        row for row in rows
        if int(row.get("prioridad", 0) or 0) > config.NOTIFY_PRIORITY_THRESHOLD
    ]

    if not priority_leads:
        return None

    lines = ["Prospeccion B2B: {0} leads de prioridad alta".format(len(priority_leads)), ""]
    for row in priority_leads[:20]:
        lines.append("- {nombre} ({industria}, {ciudad}) {email}".format(
            nombre=row.get("nombre", "?"),
            industria=row.get("industria", "?"),
            ciudad=row.get("ciudad", "?"),
            email=row.get("email", "sin email"),
        ))
    if len(priority_leads) > 20:
        lines.append("... y {0} mas".format(len(priority_leads) - 20))

    return "\n".join(lines)[:MAX_MESSAGE_LENGTH]


def enviar(texto):
    """Send a message to Telegram. Returns True when actually delivered."""
    if not texto:
        return False

    if not config.telegram_is_configured():
        print("--- Notificacion (Telegram no configurado) ---")
        print(texto)
        print("---------------------------------------------")
        return False

    try:
        response = requests.post(
            TELEGRAM_API.format(token=config.TELEGRAM_BOT_TOKEN),
            json={"chat_id": config.TELEGRAM_CHAT_ID, "text": texto},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as error:
        print("Fallo enviando la notificacion: " + type(error).__name__)
        return False


def notificar_prioritarios(rows):
    """Build and send the high-priority summary. Returns True when sent."""
    return enviar(build_summary(rows))
