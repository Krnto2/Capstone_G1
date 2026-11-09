"""
Exportación del inventario actual (material activo) a XLSX.

Hoja «Inventario general»: resumen por unidad, matriz categoría × unidad y el
detalle completo con autofiltro. Luego una hoja por unidad (carro o bodega) con
su material seccionado por cajonera. Usa la misma identidad visual del reporte
de cumplimiento (reportes/excel.py).
"""
import io
import re
from collections import Counter, defaultdict

from django.db.models import Q
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

from inventario.models import Cajonera, Material, Unidad

from .excel import (AZUL, BORDE_CELDA, CEBRA, CUERPO, GRIS_TEXTO, NEGRO, ROJO, TITULOS, _cabecera,
                    _encabezado_tabla, _preparar_impresion, _titulo_seccion, relleno)

DETALLE = [("Código", 12), ("Elemento", 34), ("Categoría", 18), ("Unidad", 10), ("Cajonera", 24), ("Tipo", 10),
           ("Cantidad", 10), ("Marca", 14), ("Modelo", 14), ("N° de serie", 16), ("Observaciones", 40)]
POR_CAJONERA = [("Código", 12), ("Elemento", 34), ("Categoría", 18), ("Tipo", 10), ("Cantidad", 10),
                ("Marca", 14), ("Modelo", 14), ("N° de serie", 16), ("Observaciones", 40)]
NUMERICAS = {"Cantidad", "Elementos", "Piezas", "Total"}
FUENTE_CODIGO = Font(name="Consolas", size=10, bold=True)


def _anchos(hoja, columnas):
    for i, (_, ancho) in enumerate(columnas, start=1):
        hoja.column_dimensions[get_column_letter(i)].width = ancho


def _fila_datos(hoja, fila, valores, cebra, encabezados=None):
    hoja.row_dimensions[fila].height = 18
    for col, valor in enumerate(valores, start=1):
        celda = hoja.cell(row=fila, column=col, value=valor)
        celda.font = Font(name=CUERPO, size=10)
        celda.border = BORDE_CELDA
        nombre = encabezados[col - 1] if encabezados and col <= len(encabezados) else ""
        if nombre in NUMERICAS or (encabezados is None and isinstance(valor, int)):
            celda.alignment = Alignment(vertical="center", horizontal="center")
        else:
            celda.alignment = Alignment(vertical="center", indent=1, wrap_text=nombre == "Observaciones")
        if nombre == "Código":
            celda.font = FUENTE_CODIGO
        if cebra:
            celda.fill = relleno(CEBRA)


def _fila_total(hoja, fila, valores):
    for col, valor in enumerate(valores, start=1):
        celda = hoja.cell(row=fila, column=col, value=valor)
        celda.font = Font(name=TITULOS, size=10, bold=True, color=NEGRO)
        celda.border = Border(top=Side(style="thin", color=NEGRO))
        celda.alignment = Alignment(vertical="center", horizontal="center" if isinstance(valor, int) else "left",
                                    indent=0 if isinstance(valor, int) else 1)


def _valores_material(m, con_ubicacion=True):
    base = [m.codigo_institucional or "s/c", m.nombre, m.categoria.nombre]
    if con_ubicacion:
        base += [m.cajonera.unidad.codigo, m.cajonera.nombre]
    return base + [m.get_tipo_display(), m.cantidad, m.marca or "", m.modelo or "", m.numero_serie or "",
                   m.observaciones or ""]


def _cuenta(n, singular, plural=None):
    return f"{n} {singular if n == 1 else (plural or singular + 's')}"


def _nombre_hoja(texto, usados):
    nombre = re.sub(r"[\[\]:*?/\\]", "-", texto).strip("' ")[:31] or "Unidad"
    base, n = nombre, 2
    while nombre.lower() in usados:
        sufijo = f" ({n})"
        nombre = base[:31 - len(sufijo)] + sufijo
        n += 1
    usados.add(nombre.lower())
    return nombre


# ------------------------------------------------------- Hoja general ----

def _hoja_general(libro, materiales, unidades):
    hoja = libro.active
    hoja.title = "Inventario general"
    hoja.sheet_properties.tabColor = AZUL
    _anchos(hoja, DETALLE)
    piezas = sum(m.cantidad for m in materiales)
    _cabecera(hoja, "Inventario de material menor",
              f"Material activo al {timezone.localtime():%d-%m-%Y} · {_cuenta(len(materiales), 'elemento')} · "
              f"{_cuenta(piezas, 'pieza')} · {_cuenta(len(unidades), 'unidad', 'unidades')}", len(DETALLE))

    # Resumen por unidad
    fila = 7
    _titulo_seccion(hoja, fila, "Resumen por unidad")
    fila += 1
    _encabezado_tabla(hoja, fila, [("Unidad", 1, 1), ("Nombre", 2, 2), ("Cajoneras", 3, 3), ("Elementos", 4, 4),
                                   ("Piezas", 5, 5)])
    por_unidad = defaultdict(list)
    for m in materiales:
        por_unidad[m.cajonera.unidad_id].append(m)
    cajoneras = Counter(Cajonera.objects.values_list("unidad_id", flat=True))
    for i, u in enumerate(unidades):
        fila += 1
        lista = por_unidad.get(u.pk, [])
        _fila_datos(hoja, fila, [u.codigo, u.nombre, cajoneras.get(u.pk, 0), len(lista),
                                 sum(m.cantidad for m in lista)], i % 2,
                    ["Código", "Nombre", "Elementos", "Elementos", "Piezas"])
    fila += 1
    _fila_total(hoja, fila, ["Total", "", sum(cajoneras.get(u.pk, 0) for u in unidades), len(materiales), piezas])

    # Matriz categoría × unidad (piezas)
    fila += 3
    _titulo_seccion(hoja, fila, "Piezas por categoría y unidad")
    fila += 1
    categorias = sorted({m.categoria.nombre for m in materiales}, key=str.lower)
    matriz = Counter()
    for m in materiales:
        matriz[(m.categoria.nombre, m.cajonera.unidad_id)] += m.cantidad
    columnas = [("Categoría", 1, 2)] + [(u.codigo, 3 + i, 3 + i) for i, u in enumerate(unidades)]
    col_total = 3 + len(unidades)
    columnas.append(("Total", col_total, col_total))
    _encabezado_tabla(hoja, fila, columnas)
    for col in range(3, col_total + 1):
        hoja.cell(row=fila, column=col).alignment = Alignment(horizontal="center", vertical="center")
        letra = get_column_letter(col)
        if hoja.column_dimensions[letra].width is None or hoja.column_dimensions[letra].width < 10:
            hoja.column_dimensions[letra].width = 10
    for i, categoria in enumerate(categorias):
        fila += 1
        hoja.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=2)
        valores = [categoria, None] + [matriz.get((categoria, u.pk)) or None for u in unidades]
        valores.append(sum(matriz.get((categoria, u.pk), 0) for u in unidades))
        _fila_datos(hoja, fila, valores, i % 2)
        for col in range(3, col_total + 1):
            hoja.cell(row=fila, column=col).alignment = Alignment(horizontal="center", vertical="center")
        hoja.cell(row=fila, column=col_total).font = Font(name=CUERPO, size=10, bold=True)
    fila += 1
    totales = [sum(m.cantidad for m in por_unidad.get(u.pk, [])) for u in unidades]
    _fila_total(hoja, fila, ["Total", ""] + totales + [piezas])
    if not categorias:
        hoja.cell(row=fila - 1, column=1, value="Sin material activo.")

    # Detalle completo
    fila += 3
    _titulo_seccion(hoja, fila, "Detalle del inventario")
    fila += 1
    fila_enc = fila
    _encabezado_tabla(hoja, fila, [(t, i, i) for i, (t, _) in enumerate(DETALLE, start=1)])
    encabezados = [t for t, _ in DETALLE]
    for i, m in enumerate(materiales):
        fila += 1
        _fila_datos(hoja, fila, _valores_material(m), i % 2, encabezados)
    if materiales:
        hoja.auto_filter.ref = f"A{fila_enc}:{get_column_letter(len(DETALLE))}{fila}"
    _preparar_impresion(hoja)


# ---------------------------------------------------- Hoja por unidad ----

def _hoja_unidad(libro, unidad, cajoneras, materiales, usados):
    hoja = libro.create_sheet(_nombre_hoja(unidad.codigo, usados))
    hoja.sheet_properties.tabColor = ROJO if unidad.tipo == "carro" else NEGRO
    _anchos(hoja, POR_CAJONERA)
    piezas = sum(m.cantidad for m in materiales)
    _cabecera(hoja, f"{unidad.codigo} · {unidad.nombre}",
              f"{unidad.get_tipo_display()} · {_cuenta(len(cajoneras), 'cajonera')} · "
              f"{_cuenta(len(materiales), 'elemento')} · {_cuenta(piezas, 'pieza')}", len(POR_CAJONERA))
    encabezados = [t for t, _ in POR_CAJONERA]
    por_cajonera = defaultdict(list)
    for m in materiales:
        por_cajonera[m.cajonera_id].append(m)

    fila = 6
    for cajonera in cajoneras:
        lista = por_cajonera.get(cajonera.pk, [])
        fila += 1
        _titulo_seccion(hoja, fila, f"{cajonera.nombre}  ·  {_cuenta(len(lista), 'elemento')} · "
                                    f"{_cuenta(sum(m.cantidad for m in lista), 'pieza')}")
        if cajonera.descripcion:
            fila += 1
            nota = hoja.cell(row=fila, column=1, value=cajonera.descripcion)
            nota.font = Font(name=CUERPO, size=9, italic=True, color=GRIS_TEXTO)
        fila += 1
        _encabezado_tabla(hoja, fila, [(t, i, i) for i, t in enumerate(encabezados, start=1)])
        for i, m in enumerate(lista):
            fila += 1
            _fila_datos(hoja, fila, _valores_material(m, con_ubicacion=False), i % 2, encabezados)
        if not lista:
            fila += 1
            hoja.cell(row=fila, column=1, value="Sin material en esta cajonera.").font = Font(
                name=CUERPO, size=10, italic=True, color=GRIS_TEXTO)
        fila += 1
    if not cajoneras:
        hoja.cell(row=7, column=1, value="Esta unidad no tiene cajoneras registradas.").font = Font(
            name=CUERPO, size=10, italic=True, color=GRIS_TEXTO)
    _preparar_impresion(hoja)
    hoja.page_setup.orientation = "landscape"


def exportar_inventario_xlsx():
    materiales = list(Material.objects.activos().con_ubicacion().order_by(
        "cajonera__unidad__codigo", "cajonera__orden", "cajonera__nombre", "nombre", "codigo_institucional"))
    con_material = {m.cajonera.unidad_id for m in materiales}
    unidades = list(Unidad.objects.filter(Q(activo=True) | Q(pk__in=con_material)).order_by("codigo"))
    cajoneras = defaultdict(list)
    for c in Cajonera.objects.filter(unidad__in=unidades).order_by("orden", "nombre"):
        cajoneras[c.unidad_id].append(c)

    libro = Workbook()
    libro.properties.title = "Inventario de material menor · SIREMA"
    libro.properties.creator = "SIREMA · Octava Compañía de Bomberos de Talcahuano"
    _hoja_general(libro, materiales, unidades)
    usados = {"inventario general"}
    for unidad in unidades:
        _hoja_unidad(libro, unidad, cajoneras[unidad.pk],
                     [m for m in materiales if m.cajonera.unidad_id == unidad.pk], usados)
    salida = io.BytesIO()
    libro.save(salida)
    return salida.getvalue()


def nombre_archivo():
    return f"inventario_sirema_{timezone.localdate():%Y%m%d}.xlsx"
