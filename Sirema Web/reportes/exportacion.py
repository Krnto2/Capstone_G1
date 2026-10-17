"""
Exportación del reporte de cumplimiento (CU-C15, RF-10): PDF, XLSX y CSV.

El PDF se genera con WeasyPrint a partir de una plantilla HTML. WeasyPrint
necesita las bibliotecas Pango del sistema, incluidas en la imagen Docker; si
no están (por ejemplo, en un equipo Windows de desarrollo) se entrega la misma
plantilla lista para imprimir o guardar como PDF desde el navegador.
"""
import base64
import csv
import io
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders

from django.template.loader import render_to_string
from django.utils import timezone

from .excel import exportar_xlsx  # noqa: F401  (diseño propio en reportes/excel.py)

ENCABEZADOS = ["Código", "Elemento", "Categoría", "Ubicación", "Plan", "Responsable", "Fecha programada",
               "Fecha límite", "Estado", "Resultado", "Ejecutada por", "Fecha de ejecución", "En plazo"]


def _fila(revision):
    material = revision.material
    en_plazo = revision.en_plazo
    return [
        material.codigo_institucional or "",
        material.nombre,
        material.categoria.nombre,
        material.ubicacion,
        str(revision.plan),
        revision.usuario_responsable.nombre_completo,
        revision.fecha_programada.strftime("%d-%m-%Y"),
        revision.fecha_limite.strftime("%d-%m-%Y"),
        revision.get_estado_display(),
        revision.get_resultado_global_display() if revision.resultado_global else "",
        revision.usuario_ejecutor.nombre_completo if revision.usuario_ejecutor else "",
        timezone.localtime(revision.fecha_hora_termino).strftime("%d-%m-%Y %H:%M") if revision.fecha_hora_termino
        else "",
        "" if en_plazo is None else ("Sí" if en_plazo else "No"),
    ]


def nombre_archivo(filtros, extension):
    return f"cumplimiento_sirema_{filtros.periodo}.{extension}"


def exportar_csv(indicadores, revisiones):
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";")
    escritor.writerow(["Reporte de cumplimiento SIREMA", indicadores.filtros.etiqueta])
    escritor.writerow(["Cumplimiento", f"{indicadores.porcentaje} %" if indicadores.porcentaje is not None else "—",
                       f"{indicadores.en_plazo} de {indicadores.exigibles} en plazo"])
    escritor.writerow([])
    escritor.writerow(ENCABEZADOS)
    for revision in revisiones:
        escritor.writerow(_fila(revision))
    return ("﻿" + salida.getvalue()).encode("utf-8")


@lru_cache(maxsize=1)
def _logo_data_uri():
    """Emblema incrustado en el HTML: sirve igual para WeasyPrint y para la vista imprimible."""
    ruta = finders.find("img/logo-8.png")
    return "data:image/png;base64," + base64.b64encode(Path(ruta).read_bytes()).decode() if ruta else ""


def _fuentes_oswald():
    """Rutas de Oswald: archivo local para WeasyPrint; la vista imprimible usa las URL estáticas."""
    rutas = {}
    for peso in (500, 700):
        ruta = finders.find(f"vendor/oswald/oswald-latin-{peso}-normal.woff2")
        rutas[peso] = Path(ruta).as_uri() if ruta else ""
    return rutas


def html_reporte(indicadores, revisiones, para_imprimir=False):
    return render_to_string("reportes/reporte_pdf.html", {
        "ind": indicadores, "revisiones": revisiones, "generado": timezone.localtime(),
        "para_imprimir": para_imprimir, "logo": _logo_data_uri(), "SIREMA_VERSION": settings.SIREMA_VERSION,
        "fuentes": None if para_imprimir else _fuentes_oswald(),
    })


def exportar_pdf(indicadores, revisiones):
    """Devuelve (bytes, True) con WeasyPrint o (html, False) si no está disponible."""
    try:
        from weasyprint import HTML
    except (ImportError, OSError):
        return html_reporte(indicadores, revisiones, para_imprimir=True), False
    return HTML(string=html_reporte(indicadores, revisiones)).write_pdf(), True
