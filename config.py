"""Central configuration and simulation-mode detection.

Every module reads its settings from here so there is a single place that
decides whether the pipeline runs against real paid APIs or against
synthetic data.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"

load_dotenv(BASE_DIR / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "").strip()
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "compass/crawler-google-places").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

SENDER_COMPANY_NAME = os.getenv("SENDER_COMPANY_NAME", "").strip()
SENDER_LEGAL_ID = os.getenv("SENDER_LEGAL_ID", "").strip()
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", "").strip()
SENDER_OPTOUT_EMAIL = os.getenv("SENDER_OPTOUT_EMAIL", "").strip()

# Model pinned explicitly. Claude Haiku 4.5, checked against the official
# model list on 2026-08-24: 1 USD/MTok input, 5 USD/MTok output.
HAIKU_MODEL = "claude-haiku-4-5-20251001"

# Cost per million tokens, used only for the local cost estimate.
HAIKU_INPUT_COST_PER_MTOK = 1.0
HAIKU_OUTPUT_COST_PER_MTOK = 5.0

# Employee band the project targets.
TARGET_MIN_EMPLOYEES = 50
TARGET_MAX_EMPLOYEES = 500

# Priority above which a lead triggers a Telegram notification.
NOTIFY_PRIORITY_THRESHOLD = 4

LEADS_RAW_CSV = DATA_DIR / "leads_raw.csv"
LEADS_ENRICHED_CSV = DATA_DIR / "leads_enriquecidos.csv"


def scraping_is_simulated():
    """Return True when no Apify token is configured."""
    return not APIFY_API_TOKEN


def classification_is_simulated():
    """Return True when no Anthropic key is configured."""
    return not ANTHROPIC_API_KEY


def telegram_is_configured():
    """Return True when both Telegram settings are present."""
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)


def ensure_directories():
    """Create the output directories if they do not exist yet."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    return True


def describe_mode():
    """Return a short human-readable description of the active mode."""
    parts = []
    parts.append("scraping=" + ("SIMULADO" if scraping_is_simulated() else "REAL"))
    parts.append(
        "clasificacion=" + ("SIMULADA" if classification_is_simulated() else "REAL")
    )
    parts.append(
        "telegram=" + ("CONFIGURADO" if telegram_is_configured() else "CONSOLA")
    )
    parts.append("envio_email=SIMULADO")
    return " | ".join(parts)
