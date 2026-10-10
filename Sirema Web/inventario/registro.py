"""
Puntos de extensión de la ficha de material (CU-B6 Consultar historial).

inventario no importa revisiones (DAS 4.3.5). Las aplicaciones que dependen
del inventario registran aquí un proveedor que aporta eventos al historial
y secciones a la ficha del elemento.
"""
_proveedores = []


def registrar_proveedor(proveedor):
    """`proveedor` expone eventos(material) -> list[dict] y secciones(material) -> list[dict]."""
    if proveedor not in _proveedores:
        _proveedores.append(proveedor)


def eventos_historial(material):
    eventos = []
    for proveedor in _proveedores:
        eventos.extend(proveedor.eventos(material))
    return eventos


def secciones_ficha(material):
    secciones = []
    for proveedor in _proveedores:
        secciones.extend(proveedor.secciones(material))
    return secciones
