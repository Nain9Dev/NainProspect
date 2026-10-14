# Security Policy

## Supported Versions
Only the latest release on the `main` branch is actively supported with security patches.

| Version | Supported |
| ------- | --------- |
| 1.0.x   | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability
If you discover a security vulnerability within NainProspect, do not open a public GitHub issue.
Report security issues privately to `security@naindev.com`.
Reports are evaluated within 48 hours.

## Data Protection & GDPR Guardrails
- **No Personal Identifiers**: The data ingestion layer deliberately strips person-specific emails (`john.doe@company.com`) and retains exclusively generic role accounts (`info@`, `contacto@`, `ventas@`).
- **No Automated Outbound**: Real cold email transmission is technically blocked in the codebase to prevent non-compliant outreach.
- **Git Isolation**: The `data/` directory and all local exports containing lead data are strictly ignored in `.gitignore`.
