# ADR-001 — Plataforma de ejecucion programada de ProspectAI

- **Identificador:** ADR-001
- **Fecha:** 2026-08-25
- **Estado:** Proposed (pendiente de aprobacion explicita)
- **Ambito:** ejecucion programada, almacenamiento de resultados y notificaciones
- **Informe completo:** https://claude.ai/code/artifact/4d47d171-0349-4696-87cf-24cf4b56610d

## Contexto y problema

El pipeline (`pipeline.py`) debe ejecutarse cada dos dias sin depender de que el PC
local este encendido, con coste cercano a cero, aislado de otros proyectos y
archivando los resultados de forma duradera. Perfil medido: ~40 MB de RAM,
3-5 min por ejecucion, ~15 ejecuciones/mes, <1 MB de salida por ejecucion.
La carga esta dominada por espera de red, no por CPU.

## Decision

**GitHub Actions en repositorio privado**, con archivado en Google Drive mediante
OAuth 2.0 de usuario y notificaciones por Telegram (ya implementadas).

## Consecuencias y compensaciones

- Consumo: 45-75 min/mes de los 2.000 incluidos en el plan Free (2-4 %).
- Sin tarjeta de credito, sin servidor que mantener, secretos cifrados con
  Libsodium y limitados a 48 KB.
- Contrapartida: el evento `schedule` puede retrasarse o descartarse en horas
  punta. No hay SLA. Mitigacion: cron fuera del minuto :00 y reejecucion manual
  con `workflow_dispatch`.
- Los artifacts (500 MB, retencion configurable) sirven como copia caliente a
  7 dias; el archivo historico vive en Google Drive.

## Alternativas rechazadas

| Opcion | Motivo del rechazo |
|---|---|
| GCP e2-micro Always Free | Requiere subir a cuenta de pago tras 90 dias o se borran los recursos; solo 3 regiones de EE. UU.; IPv4 externa facturada (~3,65 $/mes) para una VM que trabajaria 4 min cada 48 h |
| Oracle Always Free | La politica documentada reclama instancias con CPU y red <20 % en percentil 95 durante 7 dias, que es exactamente este perfil de uso; recorte de Ampere A1 a la mitad en junio de 2026 sin anuncio publico |
| Tarea programada de Cowork | Sesion de agente no determinista; sin vinculacion al equipo necesitaria clonar de GitHub igualmente; limites de ejecucion no documentados |
| PythonAnywhere Free | Sin tareas programadas para cuentas creadas despues del 2026-01-15; 100 s de CPU/dia |
| Google Colab | Sin programacion nativa fuera de Colab Enterprise / Vertex AI |
| Railway / Replit / Render / Fly.io | Ninguno ofrece cron gratuito real en 2026 |
| Cloudflare Workers | 10 ms de CPU por invocacion en el plan Free; no es Python nativo |

## Impacto de adopcion

1. Crear el repositorio privado (todavia no existe).
2. Mover `workflow_prospeccion.yml` a `.github/workflows/prospeccion.yml`.
3. Cambiar el cron de `0 7 */2 * *` a `17 7 */2 * *` (la documentacion de GitHub
   desaconseja explicitamente el minuto :00).
4. Anadir `subir_drive.py` y las dependencias `google-api-python-client` y
   `google-auth`, mas el paso de archivado en el workflow.
5. Cargar secretos y variables con `gh secret set` / `gh variable set`.

Nota sobre Google Drive: las service accounts no tienen cuota de almacenamiento
y no pueden ser propietarias de ficheros. En una cuenta de consumidor con Google
One la unica via es OAuth 2.0 con refresh token de usuario, scope `drive.file`,
y la aplicacion **publicada en produccion** (en modo Testing el refresh token
caduca a los 7 dias).

## Coste estimado

| Concepto | Coste/mes |
|---|---|
| Infraestructura (GitHub Actions) | 0,00 $ |
| Apify, hasta 1.250 fichas/mes | 0,00 $ (cubierto por el credito gratuito de 5 $, no acumulable) |
| Anthropic Haiku 4.5, 1.250 leads | ~0,85 $ |
| **Total** | **< 1 $/mes** |

Cuello de botella: el credito gratuito de Apify. `compass/crawler-google-places`
cobra 4,00 $/1.000 fichas en el tier Free, lo que fija el techo en 1.250 fichas
al mes (~83 por ejecucion).

Se mantiene Claude Haiku 4.5: es el modelo mas barato de Anthropic vigente
(Haiku 3.5 esta retirado) y el ahorro de migrar a Gemini 2.5 Flash-Lite seria de
~0,76 $/mes. El nivel gratuito de la API de Gemini usa el contenido para
entrenar, por lo que no es utilizable con datos de contacto de leads.

## Condicion para reconsiderar

- El consumo de Actions supera el 50 % de la cuota mensual (1.000 min).
- El volumen de leads exige pasar a un plan de pago de Apify.
- El pipeline pasa a necesitar estado persistente entre ejecuciones.

En ese caso, el sustituto es **Google Cloud Run Jobs + Cloud Scheduler**, cuyo
free tier cubre esta carga con holgura y que quedaria absorbido por los 10 $/mes
de credito de Google Cloud incluidos en la suscripcion de Google AI Pro.

## Bloqueante ajeno a esta decision

El envio de email comercial sigue sin implementarse a proposito. El art. 21 de la
LSSI-CE exige consentimiento previo o relacion contractual previa y protege
tambien a las personas juridicas; el art. 19 de la LOPDGDD legitima el
tratamiento del dato, no el envio. Ninguna decision de infraestructura levanta
ese gate.
