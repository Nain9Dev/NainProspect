"""Legal and compliance guardrails enforcing GDPR 6.1.f and Spanish LSSI-CE 21."""

import re
from typing import Optional

ROLE_BASED_PREFIXES = {
    "info", "contacto", "contact", "hola", "hello", "ventas", "sales",
    "comercial", "administracion", "admin", "soporte", "support", "oficina",
    "office", "general", "atencionalcliente", "clientes", "marketing",
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_role_based(email: Optional[str]) -> bool:
    """Return True only if email uses an authorized corporate role prefix.

    Personal named addresses (e.g. john.doe@company.com) return False
    to keep data collection strictly at legal entity level under GDPR.
    """
    if not email or not isinstance(email, str):
        return False

    clean_email = email.strip().lower()
    if not EMAIL_REGEX.match(clean_email):
        return False

    prefix = clean_email.split("@")[0].split("+")[0]
    return prefix in ROLE_BASED_PREFIXES


def sanitize_lead_email(email: Optional[str]) -> Optional[str]:
    """Sanitize email, discarding named individuals."""
    if is_role_based(email):
        return email.strip().lower()  # type: ignore[union-attr]
    return None


def assert_outbound_send_blocked() -> None:
    """Hard-stop check to prevent automated outbound mail transmission.

    Spanish LSSI-CE Article 21 strictly requires prior consent or an existing
    contractual relationship before sending commercial communications.
    """
    raise PermissionError(
        "Outbound cold email delivery is locked by compliance gate (LSSI-CE Art. 21). "
        "Outreach can only be simulated or reviewed manually."
    )
