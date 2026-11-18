from accesos.models import Usuario
from nucleo.enums import TipoNotificacion

from .models import Notificacion

PERMISO_JEFATURA = "panel.consultar"


def jefatura():
    return Usuario.objects.con_permiso(PERMISO_JEFATURA)


def notificar(usuario, tipo, mensaje, revision=None, unica=False):
    if usuario is None or not usuario.activo:
        return None
    if unica and Notificacion.objects.filter(usuario=usuario, tipo=tipo, revision=revision).exists():
        return None
    return Notificacion.objects.create(usuario=usuario, tipo=tipo, mensaje=mensaje[:300], revision=revision)


def notificar_jefatura(tipo, mensaje, revision=None, unica=False, excluir=()):
    creadas = []
    excluidos = {u.pk for u in excluir}
    for usuario in jefatura():
        if usuario.pk in excluidos:
            continue
        aviso = notificar(usuario, tipo, mensaje, revision, unica)
        if aviso:
            creadas.append(aviso)
    return creadas


def describir(revision):
    material = revision.material
    return f"{material.nombre} ({material.codigo_institucional or 's/c'} · {material.ubicacion})"


__all__ = ["TipoNotificacion", "notificar", "notificar_jefatura", "jefatura", "describir"]
