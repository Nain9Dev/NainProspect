"""Full prospecting pipeline: scrape, classify, report, notify.

Email sending is deliberately not implemented. The pipeline stops at
producing the classified dataset and the templates; sending real cold email
requires the legal checklist in README.md to be closed first.
"""

import argparse
import csv
import json
from datetime import datetime, timezone

import clasificador
import config
import notificaciones
import scraping

DEFAULT_QUERY = "empresas de logistica en Madrid"


def escribir_informe(rows, coste, ruta):
    """Write a plain-text report of the run."""
    en_rango = [r for r in rows if r.get("tamano_estimado") == "mediana"]
    prioritarios = [
        r for r in rows
        if int(r.get("prioridad", 0) or 0) > config.NOTIFY_PRIORITY_THRESHOLD
    ]
    con_email = [r for r in rows if r.get("email")]
    errores = [r for r in rows if r.get("estado") == "error"]

    lines = [
        "INFORME DE PROSPECCION",
        "Fecha (UTC): " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "Modo: " + config.describe_mode(),
        "",
        "Leads procesados: {0}".format(len(rows)),
        "En rango objetivo (50-500 empleados): {0}".format(len(en_rango)),
        "Con email de contacto: {0}".format(len(con_email)),
        "Prioridad > {0}: {1}".format(config.NOTIFY_PRIORITY_THRESHOLD, len(prioritarios)),
        "Errores de clasificacion: {0}".format(len(errores)),
        "",
        "COSTE DE CLASIFICACION",
        "Tokens entrada: {0}".format(coste["input_tokens"]),
        "Tokens salida: {0}".format(coste["output_tokens"]),
        "Coste de esta ejecucion: {0} USD".format(coste["coste_usd"]),
        "Extrapolado a 100 leads: {0} USD".format(coste["coste_100_leads_usd"]),
        "",
        "DETALLE",
    ]

    for row in sorted(rows, key=lambda r: -int(r.get("prioridad", 0) or 0)):
        lines.append(
            "[P{prioridad}] {nombre} | {industria} | {tamano} | conf. {confianza} | "
            "{email} | {motivo}".format(
                prioridad=row.get("prioridad", "?"),
                nombre=row.get("nombre", "?"),
                industria=row.get("industria", "?"),
                tamano=row.get("tamano_estimado", "?"),
                confianza=row.get("confianza", "?"),
                email=row.get("email") or "sin email",
                motivo=row.get("motivo", ""),
            )
        )

    ruta.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ruta


def ejecutar(query, limite, notificar=True, verbose=True):
    """Run the whole pipeline and return a result dict."""
    config.ensure_directories()

    if verbose:
        print("Modo: " + config.describe_mode())
        print("Consulta: " + query)
        print("Limite: " + str(limite))
        print("")

    leads = scraping.buscar_leads(query, limite)
    scraping.guardar_csv(leads)
    if verbose:
        print("Leads obtenidos: {0}".format(len(leads)))
        print("")

    filas, consumo = clasificador.clasificar_leads(leads, verbose=verbose)
    ruta_csv = clasificador.guardar_enriquecidos(filas)
    coste = clasificador.estimar_coste(consumo, len(filas))

    ruta_informe = config.DATA_DIR / "informe.txt"
    escribir_informe(filas, coste, ruta_informe)

    enviado = notificaciones.notificar_prioritarios(filas) if notificar else False

    return {
        "leads": filas,
        "coste": coste,
        "csv": str(ruta_csv),
        "informe": str(ruta_informe),
        "notificacion_enviada": enviado,
    }


def main():
    parser = argparse.ArgumentParser(description="Pipeline de prospeccion B2B")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Consulta de busqueda")
    parser.add_argument("--limite", type=int, default=10, help="Numero maximo de leads")
    parser.add_argument("--sin-notificar", action="store_true",
                        help="No enviar la notificacion de Telegram")
    args = parser.parse_args()

    resultado = ejecutar(args.query, args.limite, notificar=not args.sin_notificar)

    print("")
    print("CSV: " + resultado["csv"])
    print("Informe: " + resultado["informe"])
    print("Coste: " + json.dumps(resultado["coste"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
