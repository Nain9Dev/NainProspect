<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/banner-light.svg">
  <img alt="NainProspect Architectural Blueprint" src="docs/assets/banner-dark.svg" width="100%">
</picture>

# NainProspect (ProspectAI) — B2B Prospecting & Compliance Gateway

[![English](https://img.shields.io/badge/Language-English-blue?style=flat-square)](README.md)
[![Español](https://img.shields.io/badge/Idioma-Espa%C3%B1ol-emerald?style=flat-square)](README.es.md)
[![ci](https://github.com/Nain9Dev/ProspectAI/actions/workflows/ci.yml/badge.svg)](https://github.com/Nain9Dev/ProspectAI/actions/workflows/ci.yml)
[![Demo Online](https://img.shields.io/badge/demo-online-blueviolet?style=flat&logo=githubpages&logoColor=white)](https://prospect.naindev.com/)
[![Ecosystem Status](https://img.shields.io/badge/status-100%25%20operational-success)](https://status.naindev.com)
[![Engineering Handbook](https://img.shields.io/badge/paved%20road-FastAPI%20%2B%20Vue%203-blue)](https://github.com/Nain9Dev/engineering-handbook)
[![Cost](https://img.shields.io/badge/cost-0.00_%E2%82%AC-22c55e)](https://github.com/Nain9Dev/engineering-handbook/blob/main/governance/zero-cost-philosophy.md)
[![Pytest Tests](https://img.shields.io/badge/Pytest-16%2F16%20Passing-emerald?style=flat-square)](specs/001-modernization-and-showcase/tasks.md)
[![Architecture Tests](https://img.shields.io/badge/Architecture%20Tests-Clean%20Arch%20enforced-80FF00?style=flat-square&logo=checkmarx&logoColor=black)](tests/test_architecture.py)
[![Vue 3](https://img.shields.io/badge/Vue%203-Vite%206-emerald?style=flat-square)](https://prospect.naindev.com/)
[![GDPR & LSSI-CE](https://img.shields.io/badge/Compliance-LSSI--CE%20Art.%2021%20Gate-rose?style=flat-square)](docs/02-business-rules.md)

**Demo Online Interactiva:** [https://prospect.naindev.com/](https://prospect.naindev.com/)

**NainProspect** es una pasarela desacoplada de prospección B2B, enriquecimiento con IA y verificación determinista de conformidad legal dentro del ecosistema de servicios de [naindev.com](https://www.naindev.com).

Localiza empresas desde registros públicos (Apify Google Places o generadores sintéticos), extrae buzones de rol corporativo (`info@`, `contacto@`, `ventas@`), clasifica sector, tamaño de plantilla (objetivo 50-500 empleados) y prioridad (1-5) mediante Claude Haiku 4.5, y genera plantillas de outreach con pie legal inmutable.

> **Compuerta Legal Activa**: Por imperativo del artículo 21 de la LSSI-CE y el artículo 6.1.f del RGPD, el envío automático de correos en frío está técnicamente bloqueado en el código. El sistema se detiene en previsualización y simulación determinista.

---

## Matriz de Verificación en 60 Segundos

```powershell
# 1. Ejecutar la suite de pruebas unitarias e integracion (16/16 passed)
.\venv\Scripts\pytest tests/ -v

# 2. Compilar el cliente frontend Vue 3 + TypeScript (strict mode, 0 errors)
npm --prefix ProspectAI.Client run build

# 3. Lanzar la prueba CLI con 10 leads y salida por consola
.\venv\Scripts\python.exe test_pipeline.py
```

---

## Puertos y Arquitectura de Servicios

Registrado en `D:\Development\Tools\dev-ports.json`:

| Servicio | Runtime | Puerto Local | Documentación / URL |
| -------- | ------- | ------------ | ------------------- |
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

## Ejecución Local

### 1. Backend FastAPI (Puerto 8106)
```powershell
.\venv\Scripts\uvicorn src.nainprospect.main:app --port 8106 --reload
```
Accede a la documentación interactiva OpenAPI en:
`http://localhost:8106/docs`

### 2. Frontend SPA (Puerto 5377)
```powershell
cd ProspectAI.Client
npm run dev
```
Accede al panel interactivo de prospección en:
`http://localhost:5377`

### 3. Ejecución por Lotes Programada (GitHub Actions / CLI)
El script CLI original y el workflow programado `.github/workflows/prospeccion.yml` se mantienen 100% operativos:
```powershell
python pipeline.py --query "empresas de logistica en Madrid" --limite 10
```

---

## Garantías de Conformidad Legal (RGPD & LSSI-CE)

1. **Descarte de personas físicas**: La capa de ingesta (`compliance.py`) elimina cualquier dirección que no coincida con prefijos de rol de empresa (`info`, `contacto`, `ventas`, `soporte`, `comercial`, etc.).
2. **Pie legal inmutable**: El pie de los correos comerciales no lo redacta la IA; se construye determinísticamente a partir de las variables societarias (`SENDER_COMPANY_NAME`, `SENDER_LEGAL_ID`, `SENDER_ADDRESS`, `SENDER_OPTOUT_EMAIL`).
3. **Bloqueo técnico de envío**: No hay código de envío SMTP/API automático. La función `assert_outbound_send_blocked()` bloquea cualquier intento de despacho en caliente.
4. **Protección de datos en Git**: Los CSVs y datos enriquecidos se guardan en `data/` y están excluidos del repositorio en `.gitignore`.

---

## Estructura del Proyecto

```
ProspectAI/
├── AGENTS.md                          Guía técnica para desarrollo y convenciones
├── CLAUDE.md                          Restricciones arquitecturales y compliance
├── SECURITY.md                        Política de seguridad y aislamiento RGPD
├── pytest.ini                         Configuración de pruebas con pythonpath
├── requirements.txt                   Dependencias LTS de Python
├── config.py                          Configuración central y detección de modo
├── pipeline.py                        Orquestador CLI por lotes
├── test_pipeline.py                   Prueba de concepto por consola (10 leads)
├── docs/                              Documentación numerada por fases
├── src/nainprospect/                  Backend desacoplado FastAPI
│   ├── api/routes.py                  Endpoints REST
│   ├── domain/models.py               Esquemas Pydantic v2
│   ├── engine/                        Motores de sourcing, compliance y plantillas
│   └── main.py                        Punto de entrada ASGI (puerto 8106)
├── tests/                             Suite Pytest (16 tests)
└── ProspectAI.Client/                 Frontend SPA Vue 3 + TypeScript (puerto 5377)
    ├── src/components/                Componentes de control, tabla y previsualización
    ├── src/locales/                   Módulo i18n reactivo (es-ES / en-US)
    ├── src/services/api.ts            Cliente HTTP tipado
    └── vite.config.ts                 Configuración Vite con puerto 5377
```
