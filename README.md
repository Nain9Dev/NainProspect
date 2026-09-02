# Sistema de prospección B2B

Pipeline de bajo coste que localiza empresas a partir de datos públicos, las
clasifica con Claude Haiku 4.5 y genera plantillas de email. **No envía correo:
se detiene justo antes, en la simulación de envío.**

Estado actual: **prototipo local verificado en modo simulación**. No está
aprobado para tratar datos personales reales ni para lanzar campañas.

---

## Qué hace y qué no hace

| Sí | No |
|---|---|
| Scraping de fichas públicas de Google Maps vía Apify | Scraping de LinkedIn |
| Recuperar el email genérico de la web corporativa | Recuperar emails nominales de personas |
| Clasificar industria, tamaño y prioridad con Haiku 4.5 | Enviar emails reales |
| Generar tres plantillas HTML con pie legal | Gestionar bajas o supresiones automáticamente |
| Avisar por Telegram de los leads prioritarios | Guardar histórico de leads en el repositorio |

### Por qué LinkedIn no está implementado

Scrapear LinkedIn incumple de forma expresa sus condiciones de uso, y los
perfiles son datos personales de personas físicas, no datos de empresa. Si en
algún momento necesitas contacto nominal, la vía limpia es un proveedor de
datos con licencia, no un scraper.

### Qué filtra realmente el rango 50-500 empleados

Google Maps **no publica el número de empleados**. Los leads que vienen de esa
fuente llegan con `empleados_declarados` vacío, y el modelo estima la banda
marcando `confianza: baja`. Trata esas estimaciones como una señal de
priorización, no como un dato. Para filtrar de verdad por plantilla hace falta
una fuente societaria (registro mercantil, Informa, eInforma o similar), que
todavía no está integrada.

---

## Instalación en Windows

Desde PowerShell, en la carpeta del proyecto:

```powershell
python --version          # debe ser 3.11 o superior
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Si `python` no existe o es anterior a 3.11, instálalo con winget:

```powershell
winget install Python.Python.3.12
```

Después abre `.env` y rellena las claves que vayas a usar. Cada clave que dejes
vacía hace que esa parte del pipeline entre en modo simulación en lugar de
fallar, así que puedes ir habilitándolo por partes.

---

## Uso

```powershell
# Prueba completa con 10 leads, tabla en consola y previsualización del email
python test_pipeline.py

# Ejecución normal, parametrizable
python pipeline.py --query "empresas de logistica en Madrid" --limite 25

# Módulos por separado
python scraping.py "empresas de software en Valencia" 20
python clasificador.py
python generar_plantillas.py
```

Salidas, todas dentro de `data/`:

| Archivo | Contenido |
|---|---|
| `leads_raw.csv` | Lo que devuelve el scraping, sin clasificar |
| `leads_enriquecidos.csv` | Leads con industria, tamaño, prioridad y confianza |
| `informe.txt` | Resumen de la ejecución con métricas y coste real |
| `previsualizacion_envio.html` | El email que se habría enviado al mejor lead |

`data/` está en `.gitignore`. Los datos de contacto no se versionan nunca.

---

## Ejecución automática

`.github/workflows/prospeccion.yml` lanza el pipeline cada dos días a las 07:00
UTC, que son las 09:00 en Madrid en horario de verano y las 08:00 en invierno
(GitHub Actions solo admite UTC, no se ajusta solo). También se puede lanzar a
mano desde la pestaña Actions.

Configura en el repositorio, en Settings → Secrets and variables → Actions:

**Secrets:** `ANTHROPIC_API_KEY`, `APIFY_API_TOKEN`, `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`

**Variables:** `APIFY_ACTOR_ID`, `SENDER_COMPANY_NAME`, `SENDER_LEGAL_ID`,
`SENDER_ADDRESS`, `SENDER_OPTOUT_EMAIL`

Los resultados quedan como artefacto del run con retención de 7 días, no en el
repositorio.

Coste de Actions: gratis en repositorios públicos; 2.000 minutos al mes en
privados. Cada ejecución tarda un par de minutos.

---

## Estimación de coste por 100 leads

**Clasificación con Haiku 4.5** — precio verificado el 2026-08-24 en la
documentación oficial: 1 USD por millón de tokens de entrada, 5 USD por millón
de salida.

| Concepto | Cálculo | Coste |
|---|---|---|
| Entrada | ~210 tokens × 100 = 21.000 | 0,021 USD |
| Salida | ~60 tokens × 100 = 6.000 | 0,030 USD |
| **Total IA por 100 leads** | | **~0,05 USD** |

El script te da el coste **real medido** al final de cada ejecución, así que no
tienes que fiarte de esta estimación.

**Scraping con Apify** — el plan gratuito son 5 USD de crédito al mes que **no
se acumulan** y que, al agotarse, bloquean el acceso hasta el siguiente ciclo.
El precio por resultado depende del actor concreto, así que compruébalo en la
página del actor que acabes usando antes de lanzar volúmenes grandes. Esta es
la partida que realmente cuesta dinero: la IA es ruido de fondo comparada.

**Telegram y GitHub Actions:** 0 USD en este uso.

Presupuesto máximo recomendado mientras validas: 0 USD. Todo cabe en los planes
gratuitos. Antes de contratar nada, define el disparador que lo justifique
(por ejemplo, primera respuesta comercial positiva).

---

## Límites legales, pendientes antes de enviar nada real

El pipeline está construido para no meterte en un problema, pero hay decisiones
que son tuyas y no están cerradas. **No lances una campaña real hasta cerrar
esta lista:**

1. **Base jurídica documentada.** El cold email B2B se apoya en el interés
   legítimo del artículo 6.1.f del RGPD, y eso exige una evaluación de interés
   legítimo escrita, no una casilla mental.
2. **Artículo 21 de la LSSI-CE.** La comunicación comercial debe identificarse
   como tal, identificar al remitente y ofrecer una vía de baja que funcione. El
   pie legal ya lo hace, pero solo si rellenas las variables `SENDER_*`.
3. **Registro de actividades de tratamiento** que incluya esta prospección.
4. **Procedimiento de supresión.** Cuando alguien pida la baja tienes que poder
   borrarlo y no volver a contactarlo. Ahora mismo eso es manual: no hay lista
   de exclusión implementada.
5. **Política de retención.** Decide cuánto tiempo conservas un lead que no
   responde y bórralo al vencer.
6. **Latam.** Cada país tiene su propia norma (LFPDPPP en México, Ley 1581 en
   Colombia). No asumas que basta con cumplir el RGPD.

No soy abogado y esto no es asesoramiento legal. Si vas a enviar volumen real,
que lo revise alguien que lo sea.

---

## Estructura

```
prospeccion_b2b/
├── config.py               Configuración central y detección de modo simulación
├── scraping.py             Apify + enriquecimiento web, con filtro de email genérico
├── clasificador.py         Haiku 4.5, reintentos, control de coste
├── generar_plantillas.py   Plantillas HTML con pie legal determinista
├── notificaciones.py       Telegram, con fallback a consola
├── pipeline.py             Orquestador completo
├── test_pipeline.py        Prueba de concepto con 10 leads
├── .env.example            Plantilla de credenciales
├── requirements.txt
├── data/                   Salidas, ignorado por git
├── templates/              Plantillas HTML generadas
└── .github/workflows/
    └── prospeccion.yml     Ejecución cada 2 días
```

---

## Decisiones de diseño

- **Sin `lead-gen-mcp`.** El repositorio propuesto originalmente tiene 0
  estrellas y 4 commits de un autor sin trazabilidad, scrapea Google Maps (no
  empresas por plantilla) y depende de Instantly y Google Cloud. Ejecutar código
  sin auditar en la misma carpeta que un `.env` con claves de API es un riesgo
  de exfiltración innecesario. Llamar a `apify-client` directamente son 40
  líneas y ninguna superficie de ataque añadida.
- **El pie legal no lo genera el modelo.** Se construye en Python a partir de
  las variables `SENDER_*`. Lo que obliga la ley no puede depender de lo que a
  un modelo le apetezca escribir ese día.
- **Solo direcciones genéricas.** `scraping.py` descarta cualquier email cuyo
  prefijo no esté en una lista blanca de buzones de rol. Es un control técnico
  que mantiene el dataset a nivel de empresa.
- **Modo simulación por defecto.** Sin claves, el pipeline funciona entero con
  datos sintéticos. Puedes enseñar el sistema sin gastar ni un céntimo ni tocar
  un dato real.
- **Monolito de seis módulos.** No hay capas, interfaces ni inyección de
  dependencias porque a esta escala no aportan nada. Si aparece una segunda
  fuente de datos, `scraping.py` es el único punto que hay que abrir.
