# NainProspect (ProspectAI) - Developer Guide

## Architecture Overview
NainProspect is an autonomous B2B prospecting, lead enrichment, and compliance verification gateway within the NainDev ecosystem.
- **Backend**: FastAPI + Pydantic v2 application (`src/nainprospect/`) running on port `8106`.
- **Frontend**: Vue 3 + TypeScript SPA (`ProspectAI.Client/`) running on port `5377`.
- **CLI & Automation**: Dual runtime retaining scheduled batch runs via GitHub Actions (`pipeline.py`, `.github/workflows/prospeccion.yml`) and manual CLI executions.
- **Compliance Guardrail**: Enforces GDPR Article 6.1.f (legitimate interest) and Spanish LSSI-CE Article 21. Real email delivery is locked behind a strict compliance gate; all outreach templates are rendered in simulation mode.

## Development Commands

### Backend (Python 3.12+)
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Run unit and integration tests
.\venv\Scripts\pytest tests/ -v

# Run FastAPI dev server (port 8106)
.\venv\Scripts\uvicorn src.nainprospect.main:app --port 8106 --reload

# Run legacy CLI pipeline in simulation mode
python pipeline.py --query "empresas de logistica en Madrid" --limite 10
```

### Frontend (Vue 3 + TypeScript)
```powershell
cd ProspectAI.Client
npm install
npm run dev      # Serves on http://localhost:5377
npm run build    # Type-check with vue-tsc and build
```

## Ports and Boundaries
- Frontend UI: `http://localhost:5377`
- Backend API & OpenAPI Specs: `http://localhost:8106/docs`
- Health check: `http://localhost:8106/health`
