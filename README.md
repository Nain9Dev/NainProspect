# NainProspect (ProspectAI) — B2B Prospecting & Compliance Gateway

[![Pytest Tests](https://img.shields.io/badge/Pytest-15%2F15%20Passing-emerald?style=flat-square)](specs/001-modernization-and-showcase/tasks.md)
[![FastAPI](https://img.shields.io/badge/FastAPI-8106-blue?style=flat-square)](http://localhost:8106/docs)
[![Vue 3](https://img.shields.io/badge/Vue%203-5377-emerald?style=flat-square)](http://localhost:5377)
[![GDPR & LSSI-CE](https://img.shields.io/badge/Compliance-LSSI--CE%20Art.%2021%20Gate-rose?style=flat-square)](docs/02-business-rules.md)

**NainProspect** es una pasarela desacoplada de prospección B2B, enriquecimiento con IA y verificación determinista de conformidad legal dentro del ecosistema de servicios de [naindev.com](https://www.naindev.com).

Localiza empresas desde registros públicos (Apify Google Places o generadores sintéticos), extrae buzones de rol corporativo (`info@`, `contacto@`, `ventas@`), clasifica sector, tamaño de plantilla (objetivo 50-500 empleados) y prioridad (1-5) mediante Claude Haiku 4.5, y genera plantillas de outreach con pie legal inmutable.

> **Compuerta Legal Activa**: Por imperativo del artículo 21 de la LSSI-CE y el artículo 6.1.f del RGPD, el envío automático de correos en frío está técnicamente bloqueado en el código. El sistema se detiene en previsualización y simulación determinista.

---

## Matriz de Verificación en 60 Segundos

```powershell
# 1. Ejecutar la suite de pruebas unitarias e integracion (15/15 passed)
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

```
+-------------------------------------------------------------+
|              ProspectAI.Client (Vue 3 + TS)                |
|        Puerto 5377 - Dark Glassmorphism SPA                |
+------------------------------+------------------------------+
                               | HTTP / JSON (Proxy :5377/api)
                               v
+-------------------------------------------------------------+
|               FastAPI Service (src/nainprospect)            |
|                   Puerto 8106 - Python 3.12                 |
|  +--------------------+   +-------------------------------+ |
|  | Pipeline REST API  |   | Template & Compliance API     | |
|  +---------+----------+   +---------------+---------------+ |
|            |                              |                 |
|            v                              v                 |
|  +--------------------+   +-------------------------------+ |
|  | Sourcing Engine    |   | Claude Haiku 4.5 / Heuristica | |
|  | (Apify / Fixtures) |   | Clasificador de Prioridad     | |
|  +---------+----------+   +---------------+---------------+ |
|            |                              |                 |
|            v                              v                 |
|  +--------------------+   +-------------------------------+ |
|  | Filtro de Buzon    |   | Pie Legal Determinista        | |
|  | Rol Corporativo    |   | LSSI-CE 21 & RGPD 6.1.f       | |
|  +--------------------+   +-------------------------------+ |
+-------------------------------------------------------------+
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
│   ├── 00-charter.md                  Carta del proyecto
│   ├── 01-architecture.md             Topología y contratos
│   ├── 02-business-rules.md           Reglas de negocio y compuertas legales
│   ├── 03-decisions/                  Registro de decisiones arquitecturales
│   │   ├── ADR-001-scheduled-infrastructure.md
│   │   └── ADR-002-fastapi-and-vue-client.md
│   ├── changelog.md                   Historial de versiones
│   └── traceability.md                Matriz de trazabilidad
├── specs/                             Especificaciones de características
│   └── 001-modernization-and-showcase/
├── src/nainprospect/                  Backend desacoplado FastAPI
│   ├── api/routes.py                  Endpoints REST
│   ├── domain/models.py               Esquemas Pydantic v2
│   ├── engine/                        Motores de sourcing, compliance y plantillas
│   └── main.py                        Punto de entrada ASGI (puerto 8106)
├── tests/                             Suite Pytest (15 tests)
└── ProspectAI.Client/                 Frontend SPA Vue 3 + TypeScript (puerto 5377)
    ├── src/components/                Componentes de control, tabla y previsualización
    ├── src/services/api.ts            Cliente HTTP tipado
    └── vite.config.ts                 Configuración Vite con puerto 5377
```
