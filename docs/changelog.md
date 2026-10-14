# Changelog — NainProspect (ProspectAI)

All notable changes to this project are documented in this file following Keep a Changelog and Semantic Versioning.

## [1.0.0] - 2026-10-14
### Added
- Modular FastAPI backend application in `src/nainprospect/` running on port 8106.
- Pydantic v2 domain schemas (`RawLead`, `EnrichedLead`, `PipelineRun`, `TemplatePreview`, `CostMetrics`).
- Reactive Vue 3 + TypeScript client in `ProspectAI.Client/` running on port 5377 with dark glassmorphic design system.
- Dual-mode thread-safe pipeline store with built-in synthetic benchmark leads generator.
- Interactive live template renderer with deterministic LSSI-CE 21 legal footers.
- Automated unit and integration test suite in `tests/` with pytest.
- Scalar OpenAPI interactive reference documentation at `/docs`.
- Standard governance suite (`AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, `pytest.ini`, `.editorconfig`, `docs/`, `specs/`).

### Changed
- Refactored core modules to support both CLI invocation and asynchronous REST execution.
- Registered port allocations in `D:\Development\Tools\dev-ports.json` (Web: 5377, API: 8106).
