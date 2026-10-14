# Architecture Specification — NainProspect

## 1. System Topology

```
+-----------------------------------------------------------+
|              ProspectAI.Client (Vue 3 + TS)              |
|        Port 5377 - NainDev Dark Glassmorphism SPA         |
+-----------------------------+-----------------------------+
                              | HTTP / JSON
                              v
+-----------------------------------------------------------+
|               FastAPI Service (src/nainprospect)          |
|                   Port 8106 - Python 3.12                 |
|  +--------------------+  +-----------------------------+  |
|  | Lead Pipeline API  |  | Template & Compliance API   |  |
|  +---------+----------+  +--------------+--------------+  |
|            |                            |                 |
|            v                            v                 |
|  +--------------------+  +-----------------------------+  |
|  | In-Memory / SQLite |  | Claude Haiku 4.5 / Heuristic|  |
|  | Pipeline Store     |  | AI Classifier               |  |
|  +---------+----------+  +--------------+--------------+  |
|            |                            |                 |
|            v                            v                 |
|  +--------------------+  +-----------------------------+  |
|  | Web Scraper &      |  | LSSI-CE 21 Deterministic    |  |
|  | Role-Based Filter  |  | Legal Footer Generator      |  |
|  +--------------------+  +-----------------------------+  |
+-----------------------------------------------------------+
```

## 2. Component Breakdown

### 2.1 Backend Modules (`src/nainprospect/`)
- `domain/models.py`: Pydantic v2 schemas for `RawLead`, `EnrichedLead`, `PipelineRun`, `ClassificationRequest`, `TemplatePreview`, `CostMetrics`.
- `engine/sourcing.py`: Extracts leads from Apify Google Places or synthetic fixture generators; runs web scrapers for role-based contact addresses.
- `engine/compliance.py`: Discards named individuals (`john@...`), validates corporate roles (`info@`, `contacto@`), constructs immutable legal footers per LSSI-CE 21.
- `engine/classifier.py`: Calls Claude Haiku 4.5 (or fallback rule engine in simulation mode) to determine industry, company size, and priority score (1-5).
- `engine/templates.py`: Injects company and contact metadata into industry-specific outreach templates (`retail`, `tecnologia`, `logistica`).
- `engine/storage.py`: Thread-safe dual-mode storage engine (in-memory / SQLite) ensuring privacy compliance.
- `api/routes.py`: FastAPI routes providing endpoints for run triggers, lead listings, template previews, and cost audits.

### 2.2 Frontend SPA (`ProspectAI.Client/`)
- Framework: Vue 3 (Composition API) with strict TypeScript, Vite 6, and Vanilla CSS.
- Port: `5377` (governed by `D:\Development\Tools\dev-ports.json`).
- Key Views & Components:
  - `HeaderNav.vue`: Branding (`NainProspect`), runtime mode indicator, server health probe.
  - `PipelineControl.vue`: Search query, limit parameter, simulation mode toggles, one-click run trigger.
  - `LeadsTable.vue`: Interactive table with priority badges, confidence pills, sector tags, and search filter.
  - `TemplateViewer.vue`: Live rendered email preview with deterministic legal footer.
  - `CostMetricsCard.vue`: Token consumption counters and dollar-cost breakdown.
