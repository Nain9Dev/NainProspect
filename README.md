<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/banner-light.svg">
  <img alt="NainProspect Architectural Blueprint" src="docs/assets/banner-dark.svg" width="100%">
</picture>

# NainProspect (ProspectAI) — B2B Prospecting & Compliance Gateway

[![English](https://img.shields.io/badge/Language-English-blue?style=flat-square)](README.md)
[![Español](https://img.shields.io/badge/Idioma-Espa%C3%B1ol-emerald?style=flat-square)](README.es.md)
[![ci](https://github.com/Nain9Dev/ProspectAI/actions/workflows/ci.yml/badge.svg)](https://github.com/Nain9Dev/ProspectAI/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/demo-online-blueviolet?style=flat&logo=githubpages&logoColor=white)](https://prospect.naindev.com/)
[![Ecosystem Status](https://img.shields.io/badge/status-100%25%20operational-success)](https://status.naindev.com)
[![Engineering Handbook](https://img.shields.io/badge/paved%20road-FastAPI%20%2B%20Vue%203-blue)](https://github.com/Nain9Dev/engineering-handbook)
[![Cost](https://img.shields.io/badge/cost-0.00_%E2%82%AC-22c55e)](https://github.com/Nain9Dev/engineering-handbook/blob/main/governance/zero-cost-philosophy.md)
[![Pytest Tests](https://img.shields.io/badge/Pytest-16%2F16%20Passing-emerald?style=flat-square)](specs/001-modernization-and-showcase/tasks.md)
[![Architecture Tests](https://img.shields.io/badge/Architecture%20Tests-Clean%20Arch%20enforced-80FF00?style=flat-square&logo=checkmarx&logoColor=black)](tests/test_architecture.py)
[![Vue 3](https://img.shields.io/badge/Vue%203-Vite%206-emerald?style=flat-square)](https://prospect.naindev.com/)
[![GDPR & LSSI-CE](https://img.shields.io/badge/Compliance-LSSI--CE%20Art.%2021%20Gate-rose?style=flat-square)](docs/02-business-rules.md)

**Interactive Live Demo:** [https://prospect.naindev.com/](https://prospect.naindev.com/)

**NainProspect** is a decoupled B2B prospecting, AI enrichment, and deterministic legal compliance gateway within the [naindev.com](https://www.naindev.com) service ecosystem.

It sources company data from public registries (Apify Google Places or synthetic fixtures), extracts corporate role mailboxes (`info@`, `contacto@`, `ventas@`), classifies business sector, headcount band (target 50-500 employees), and priority score (1-5) via Claude Haiku 4.5, and generates compliant outreach drafts with an immutable legal footer.

> **Active Safety Gate**: By mandate of Spanish LSSI-CE Article 21 and GDPR Article 6.1.f, automated cold emailing is technically blocked in the codebase. The pipeline stops deterministically at preview and audit simulation.

---

## 60-Second Verification Matrix

```powershell
# 1. Run unit, integration, and architecture test suite (16/16 passed)
.\venv\Scripts\pytest tests/ -v

# 2. Build Vue 3 + TypeScript frontend client (strict mode, 0 errors)
npm --prefix ProspectAI.Client run build

# 3. Execute CLI pipeline test with 10 synthetic leads
.\venv\Scripts\python.exe test_pipeline.py
```

---

## Ports and Service Architecture

Registered in `D:\Development\Tools\dev-ports.json`:

| Service | Runtime | Local Port | Documentation / URL |
| ------- | ------- | ---------- | -------------------- |
| **ProspectAI.Client** | Vue 3 + TypeScript (Vite 6) | `5377` | `http://localhost:5377` |
| **FastAPI Backend** | Python 3.12 + Pydantic v2 | `8106` | `http://localhost:8106/docs` (Scalar) |
| **Health Probe** | ASGI Health Endpoint | `8106` | `http://localhost:8106/health` |

```mermaid
graph TB
    subgraph ClientLayer["Frontend Client Layer (:5377)"]
        VueClient["ProspectAI.Client<br/><code>Vue 3 + TypeScript (Vite 6)</code><br/><i>Dark Glassmorphism SPA // prospect.naindev.com</i>"]
    end

    subgraph ServiceLayer["FastAPI Service Layer (:8106)"]
        FastApiApp["FastAPI REST Application<br/><code>Python 3.12 + Pydantic v2</code><br/><i>ASGI Async Pipeline Router</i>"]
        
        subgraph IngestionSub["Data Sourcing &amp; Sanitization"]
            Sourcing["Sourcing Engine<br/><i>Apify Google Places / Fixtures</i>"]
            MailboxFilter["Corporate Mailbox Guard<br/><i>Filters <code>info@</code>, <code>ventas@</code> / Blocks PII</i>"]
        end

        subgraph IntelligenceSub["Classification &amp; Compliance Engine"]
            Classifier["Claude Haiku 4.5 &amp; Heuristic Classifier<br/><i>Priority Scoring (1-5) &amp; Headcount Fit</i>"]
            TemplateGen["Outreach Template Engine<br/><i>Sector Specialization &amp; Personalization</i>"]
            LegalGate["LSSI-CE Art. 21 &amp; RGPD 6.1.f Gate<br/><b>FAIL-CLOSED: Hard-blocked Outbound Send</b>"]
        end
    end

    VueClient -->|"HTTP / REST API (Proxy :5377/api)"| FastApiApp
    FastApiApp --> Sourcing
    Sourcing --> MailboxFilter
    MailboxFilter --> Classifier
    Classifier --> TemplateGen
    TemplateGen --> LegalGate
    LegalGate -.->|"Preview &amp; Audit Logs Only"| VueClient

    classDef client fill:#0047AB,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF;
    classDef gateway fill:#002B66,stroke:#80FF00,stroke-width:2px,color:#FFFFFF;
    classDef comp fill:#060D1A,stroke:#38BDF8,stroke-width:2px,color:#FFFFFF;
    classDef gate fill:#4C0519,stroke:#FB7185,stroke-width:2px,color:#FFFFFF;

    class VueClient client;
    class FastApiApp,Sourcing,MailboxFilter gateway;
    class Classifier,TemplateGen comp;
    class LegalGate gate;
```

---

## Local Execution

### 1. Backend FastAPI (Port 8106)
```powershell
.\venv\Scripts\uvicorn src.nainprospect.main:app --port 8106 --reload
```
Interactive OpenAPI / Scalar documentation is available at:
`http://localhost:8106/docs`

### 2. Frontend SPA (Port 5377)
```powershell
cd ProspectAI.Client
npm run dev
```
Interactive prospecting dashboard is available at:
`http://localhost:5377`

### 3. Scheduled Batch Execution (CLI / GitHub Actions)
The CLI script and scheduled workflow `.github/workflows/prospeccion.yml` remain fully operational:
```powershell
python pipeline.py --query "logistics companies in Madrid" --limite 10
```

---

## Legal Compliance Guarantees (GDPR & LSSI-CE)

1. **PII and Natural Person Mailbox Discard**: The ingestion layer (`compliance.py`) strictly eliminates any email address not matching standard corporate role prefixes (`info`, `contacto`, `ventas`, `soporte`, `comercial`, etc.).
2. **Deterministic Legal Footer**: Outreach footers are never generated stochastically by LLMs; they are constructed deterministically in code from statutory corporate attributes (`SENDER_COMPANY_NAME`, `SENDER_LEGAL_ID`, `SENDER_ADDRESS`, `SENDER_OPTOUT_EMAIL`).
3. **Fail-Closed Sending Barrier**: No automated SMTP or transactional API dispatch routines exist. The `assert_outbound_send_blocked()` function blocks any execution attempting outbound dispatch.
4. **Data Isolation**: Ingested datasets and generated CSV artifacts are persisted to `data/` and excluded from source control via `.gitignore`.

---

## Repository Structure

```
ProspectAI/
├── AGENTS.md                          Developer conventions and operational constraints
├── CLAUDE.md                          Architectural boundaries and compliance rules
├── SECURITY.md                        Security policy and GDPR isolation guarantees
├── pytest.ini                         Test configuration with pythonpath
├── requirements.txt                   Pinned LTS Python dependencies
├── config.py                          Central configuration and mode detector
├── pipeline.py                        CLI batch orchestrator
├── test_pipeline.py                   Console proof-of-concept runner (10 leads)
├── docs/                              Numbered lifecycle documentation
├── src/nainprospect/                  Decoupled FastAPI backend
│   ├── api/routes.py                  REST endpoints
│   ├── domain/models.py               Pydantic v2 schemas
│   ├── engine/                        Sourcing, compliance, and template engines
│   └── main.py                        ASGI application entrypoint (port 8106)
├── tests/                             Pytest suite (16 tests)
└── ProspectAI.Client/                 Vue 3 + TypeScript SPA (port 5377)
    ├── src/components/                Control, table, and preview modal components
    ├── src/locales/                   Reactive i18n module (es-ES / en-US)
    ├── src/services/api.ts            Typed HTTP client
    └── vite.config.ts                 Vite configuration pinned to port 5377
```
