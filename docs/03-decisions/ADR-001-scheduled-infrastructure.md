# ADR-001 — Scheduled Execution and Archival Platform for ProspectAI

- **Status**: Approved
- **Date**: 2026-08-25
- **Deciders**: naindev
- **Scope**: Automated scheduled runs, pipeline outputs archival, and notification channels.

## Context
The pipeline needs to run periodically without requiring a local machine to be turned on, maintaining near-zero operating cost, isolated execution, and durable output archiving. Measured footprint: ~40 MB RAM, 3-5 min per run, ~15 runs/month, <1 MB output per run.

## Decision
Run the pipeline via **GitHub Actions** (`.github/workflows/prospeccion.yml`) on a private repository schedule (`17 7 */2 * *`), archive historical artifacts into Google Drive using OAuth 2.0 user credentials with refresh tokens, and send priority alerts via Telegram.

## Consequences
- Free tier usage stays under 2-4% of available monthly minutes.
- Secrets securely managed in GitHub Actions.
- Fail-closed: missing tokens or keys automatically degrade to simulation mode without failing the workflow.
