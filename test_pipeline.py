"""Proof of concept: 10 leads end to end, printed as a table.

No email is ever sent. The last step only renders the template that WOULD be
used for the top lead, so you can eyeball the result before anything real
leaves the machine.
"""

import config
import generar_plantillas
import pipeline

LIMITE_PRUEBA = 10
CONSULTA_PRUEBA = "empresas de logistica en Madrid"


def imprimir_tabla(rows):
    """Print the classified leads as a fixed-width table."""
    header = "{0:<34} {1:<13} {2:<12} {3:>4}  {4:<8} {5}".format(
        "EMPRESA", "INDUSTRIA", "TAMANO", "PRIO", "CONF", "EMAIL")
    print(header)
    print("-" * len(header))
    for row in sorted(rows, key=lambda r: -int(r.get("prioridad", 0) or 0)):
        print("{0:<34} {1:<13} {2:<12} {3:>4}  {4:<8} {5}".format(
            row.get("nombre", "?")[:34],
            row.get("industria", "?")[:13],
            row.get("tamano_estimado", "?")[:12],
            row.get("prioridad", "?"),
            row.get("confianza", "?")[:8],
            row.get("email") or "sin email",
        ))


def simular_envio(rows):
    """Show which template would be used for the best lead. Sends nothing."""
    candidatos = [
        r for r in rows
        if int(r.get("prioridad", 0) or 0) > config.NOTIFY_PRIORITY_THRESHOLD
        and r.get("email")
    ]
    if not candidatos:
        print("Ningun lead supera el umbral de prioridad con email valido.")
        return None

    lead = candidatos[0]
    sector = lead.get("industria")
    if sector not in generar_plantillas.SECTORS:
        sector = "tecnologia"

    plantilla = config.TEMPLATES_DIR / "{0}.html".format(sector)
    if not plantilla.exists():
        print("Falta la plantilla " + str(plantilla))
        return None

    html = plantilla.read_text(encoding="utf-8")
    html = html.replace("{{NOMBRE_EMPRESA}}", lead.get("nombre", ""))
    html = html.replace("{{CIUDAD}}", lead.get("ciudad", ""))
    html = html.replace("{{INDUSTRIA}}", lead.get("industria", ""))
    html = html.replace("{{EMAIL_LEAD}}", lead.get("email", ""))

    destino = config.DATA_DIR / "previsualizacion_envio.html"
    destino.write_text(html, encoding="utf-8")

    print("")
    print("SIMULACION DE ENVIO (no se envia nada)")
    print("  Destinatario que se usaria: " + lead.get("email", ""))
    print("  Plantilla: " + sector)
    print("  Previsualizacion: " + str(destino))
    return destino


def main():
    print("=" * 78)
    print("PRUEBA DE CONCEPTO - PIPELINE DE PROSPECCION B2B")
    print("=" * 78)
    print("")

    generar_plantillas.generar_plantillas()
    print("")

    resultado = pipeline.ejecutar(CONSULTA_PRUEBA, LIMITE_PRUEBA, notificar=True)

    print("")
    imprimir_tabla(resultado["leads"])

    simular_envio(resultado["leads"])

    coste = resultado["coste"]
    print("")
    print("COSTE")
    print("  Esta ejecucion: {0} USD".format(coste["coste_usd"]))
    print("  Por lead: {0} USD".format(coste["coste_por_lead_usd"]))
    print("  Extrapolado a 100 leads: {0} USD".format(coste["coste_100_leads_usd"]))
    print("")
    print("Informe completo: " + resultado["informe"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
