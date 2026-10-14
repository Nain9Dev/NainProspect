# NainProspect — Project Guidelines

## Codebase Structure
- `src/nainprospect/domain/`: Pydantic v2 schemas (`Lead`, `EnrichedLead`, `PipelineRun`, `TemplatePreview`, `CostMetrics`).
- `src/nainprospect/engine/`: Sourcing scrapers, generic email filtering, AI classification engine, template renderer.
- `src/nainprospect/api/`: FastAPI routers (`/api/leads`, `/api/pipeline`, `/api/templates`, `/api/metrics`).
- `src/nainprospect/main.py`: ASGI entrypoint with CORS, health checks, and OpenAPI Scalar documentation.
- `ProspectAI.Client/`: Vue 3 + TypeScript single-page application with NainDev glassmorphic UI.
- `tests/`: Automated unit and integration test suite using pytest.
- `pipeline.py`, `clasificador.py`, `scraping.py`, `generar_plantillas.py`: CLI scripts preserved for standalone automation.

## Constraints & Rules
- Language: Technical English for code, schemas, and commits. Spanish for user-facing UI copy and legal disclaimers.
- Style: Conventional Commits, no emojis, strict typing, no AI watermarks.
- Privacy & GDPR: Personal named emails must be discarded. Only role-based corporate addresses (`info@`, `contacto@`, etc.) are retained.
- Email Gate: Never send cold emails automatically. The delivery stage remains locked in simulation mode.
