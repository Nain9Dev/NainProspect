# Changelog — NainProspect (ProspectAI)

All notable changes to this project are documented in this file following Keep a Changelog and Semantic Versioning.

## [Unreleased]
### Added
- Showcase header and guided scenario in the client (`specs/002-showcase-header`): what the product does, in Spanish and English, and a button that runs the whole pipeline on synthetic data stage by stage (capture, classification, compliance, outreach). Every figure is computed from the leads the run returned; at the end it offers the generated email of the best qualified lead. Real sending stays blocked and the header says so.
- `npm test` in `ProspectAI.Client` (Node test runner, no new dependency) covering the scenario logic.

### Fixed
- The page scrolled sideways on a phone (about 950 px wide): the header row and the single grid column took the width of their content. They now wrap and the column can shrink.
- The fixed NainDev suite bar covered the top of the header; the body now reserves its height once the bar is defined.

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
