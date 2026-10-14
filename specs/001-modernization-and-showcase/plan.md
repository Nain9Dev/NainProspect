# Technical Implementation Plan: NainProspect

## 1. Domain & Architecture Design
1. Define Pydantic v2 domain schemas in `src/nainprospect/domain/models.py`.
2. Extract and refine core logic into modular engines (`sourcing`, `compliance`, `classifier`, `templates`, `storage`).
3. Implement thread-safe dual storage (in-memory + SQLite fallback) and synthetic dataset generation.

## 2. API & Service Layer
1. Build FastAPI application in `src/nainprospect/main.py` and `src/nainprospect/api/routes.py`.
2. Provide endpoints:
   - `GET /health` and `GET /health/ready`
   - `GET /api/config`
   - `POST /api/pipeline/run`
   - `GET /api/leads`
   - `GET /api/leads/{id}`
   - `GET /api/templates`
   - `GET /api/templates/{sector}/preview`
   - `GET /api/metrics`
3. Include Scalar OpenAPI documentation on `/docs`.

## 3. Frontend Architecture
1. Scaffold Vue 3 + TypeScript project in `ProspectAI.Client/`.
2. Configure `vite.config.ts` with pinned port `5377`, strictPort, and proxy to `http://localhost:8106`.
3. Build components: `HeaderNav.vue`, `PipelineControl.vue`, `LeadsTable.vue`, `TemplateViewer.vue`, `CostMetricsCard.vue`.

## 4. Testing & Verification
1. Pytest suite covering compliance rules, lead filtering, template rendering, and API routes.
2. Production build verification of frontend (`vue-tsc -b && vite build`).
