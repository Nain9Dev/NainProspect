# ADR-002 — Modernization to Decoupled FastAPI and Vue 3 Architecture

- **Status**: Approved
- **Date**: 2026-10-14
- **Deciders**: naindev
- **Scope**: REST API, Web Presentation, and Ecosystem Integration with naindev.com.

## Context
ProspectAI originally existed solely as a Python CLI script and a GitHub Actions cron job. To serve as an interactive microservice and commercial showcase within the `naindev.com` platform (aligned with `NainPolicy`, `NainConfigurator`, `NainOrder`, `Nain3D`), the project requires an interactive web UI, structured Pydantic v2 domain schemas, OpenAPI documentation, and local port allocation.

## Decision
1. **Commercial Brand**: Adopt **NainProspect** (or **NainProspect Gateway**) as the public commercial identity while keeping the repository named `ProspectAI`.
2. **Backend**: Implement a modular FastAPI service (`src/nainprospect/`) on port `8106` using Pydantic v2 schemas and Scalar OpenAPI documentation on `/docs`.
3. **Frontend**: Implement a reactive Vue 3 + TypeScript SPA (`ProspectAI.Client/`) on port `5377` adhering to NainDev's dark glassmorphism design standard.
4. **Dual Runtime**: Preserve full backward compatibility with the CLI pipeline (`pipeline.py`) and GitHub Actions workflow (`prospeccion.yml`).
5. **Storage**: In-memory / SQLite pipeline store with procedural synthetic lead generator for demo sessions without storing real PII in git.

## Consequences
- Allows live testing and portfolio presentation without incurring API costs.
- Decouples UI presentation from backend lead generation and compliance engines.
- Strict GDPR compliance preserved: real cold email dispatch remains hard-locked in simulation mode.
