"""
Capa de servicios del inventario (IInventario).

Revisiones consulta el inventario a través de estas funciones y de los gestores
del modelo Material, sin escribir directamente sus tablas.
"""
from django.core.exceptions import ValidationError
from django.db import transaction

from accesos import auditoria
from nucleo.enums import AccionAuditoria, TipoMaterial
from nucleo.utilidades import normalizar_codigo

from .models import Material, Movimiento

CAMPOS_FICHA = ["codigo_institucional", "nombre", "categoria", "cajonera", "tipo", "cantidad",
                "marca", "modelo", "numero_serie", "observaciones"]


def verificar_codigo(codigo, excluir_pk=None):
    """RF-04: rechaza un código repetido indicando a qué elemento pertenece."""
    codigo = normalizar_codigo(codigo)
    if not codigo:
        return None
    existente = Material.objects.filter(codigo_institucional__iexact=codigo).exclude(pk=excluir_pk).first()
    if existente:
        estado = "dado de baja" if not existente.activo else "activo"
        raise ValidationError(f"El código {codigo} ya pertenece a «{existente.nombre}» ({estado}).",
                              code="codigo_duplicado")
    return codigo


def validar_ficha(datos):
    """Reglas de la ficha comunes al formulario y a la carga masiva."""
    errores = {}
    if datos.get("tipo") == TipoMaterial.UNITARIO:
        if not datos.get("codigo_institucional"):
            errores["codigo_institucional"] = "El código institucional es obligatorio para el material unitario."
        if datos.get("cantidad") not in (None, 1):
            errores["cantidad"] = "El material unitario tiene cantidad 1."
    if errores:
        raise ValidationError(errores)


def registrar_material(datos, usuario):
    """CU-B1: guarda el elemento activo y su ubicación inicial como primer movimiento."""
    datos = {k: v for k, v in datos.items() if k in CAMPOS_FICHA}
    datos["codigo_institucional"] = verificar_codigo(datos.get("codigo_institucional"))
    if datos.get("tipo") == TipoMaterial.UNITARIO:
        datos["cantidad"] = 1
    validar_ficha(datos)
    with transaction.atomic():
        material = Material.objects.create(**datos)
        Movimiento.objects.create(material=material, cajonera_origen=None, cajonera_destino=material.cajonera,
                                  usuario=usuario, motivo="Alta inicial")
        auditoria.registrar(AccionAuditoria.ALTA, "material", material.pk,
                            nuevos=auditoria.instantanea(material), usuario=usuario)
    return material


def modificar_material(material, datos, usuario):
    """CU-B2: modifica la ficha. La ubicación cambia solo mediante un movimiento."""
    anteriores = auditoria.instantanea(Material.objects.get(pk=material.pk))
    datos = {k: v for k, v in datos.items() if k in CAMPOS_FICHA and k != "cajonera"}
    datos["codigo_institucional"] = verificar_codigo(datos.get("codigo_institucional"), excluir_pk=material.pk)
    if datos.get("tipo") == TipoMaterial.UNITARIO:
        datos["cantidad"] = 1
    validar_ficha(datos)
    with transaction.atomic():
        for campo, valor in datos.items():
            setattr(material, campo, valor)
        material.save()
        antes, despues = auditoria.diferencias(anteriores, auditoria.instantanea(material))
        antes.pop("fecha_actualizacion", None)
        despues.pop("fecha_actualizacion", None)
        if despues:
            auditoria.registrar(AccionAuditoria.MODIFICACION, "material", material.pk, antes, despues,
                                usuario=usuario)
    return material


def elementos_asignables(texto=None):
    """Elementos activos que pueden recibir un plan (CU-C3 incluye CU-B4)."""
    return Material.objects.activos().con_ubicacion().buscar(texto)
