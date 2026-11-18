_proveedores = []


def registrar_proveedor(proveedor):
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
