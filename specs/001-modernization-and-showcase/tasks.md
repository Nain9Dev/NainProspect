# Implementation Tasks — NainProspect

- [x] [A] Initialize repository governance (`.editorconfig`, `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, `pytest.ini`).
- [x] [A] Register development ports in `D:\Development\Tools\dev-ports.json` (Client: 5377, API: 8106).
- [ ] [A] Implement Pydantic v2 domain schemas (`src/nainprospect/domain/models.py`).
- [ ] [A] Implement modular engines (`compliance.py`, `sourcing.py`, `classifier.py`, `templates.py`, `storage.py`).
- [ ] [A] Build FastAPI REST API and application entrypoint (`src/nainprospect/api/routes.py`, `src/nainprospect/main.py`).
- [ ] [A] Create comprehensive Pytest suite in `tests/` (`test_compliance.py`, `test_templates.py`, `test_api.py`).
- [ ] [A] Scaffold and build reactive Vue 3 + TypeScript client (`ProspectAI.Client/`) with dark glassmorphism styling.
- [ ] [A] Verify all Pytest tests (100% pass) and frontend type-checking / production build.
- [ ] [A] Rewrite `README.md` with 60-second test matrix, architecture diagram, and operational guides.
