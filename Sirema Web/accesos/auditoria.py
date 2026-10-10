"""
IAuditoria: registro de eventos en la bitácora (RNF-09).

El middleware deja disponibles el usuario y la IP de cada solicitud, de modo
que los servicios de cualquier aplicación registren eventos sin recibir el
request. Las acciones automáticas se atribuyen al usuario técnico «sistema».
"""
import contextvars
import datetime
import decimal
import uuid

from django.db import models

from nucleo.enums import AccionAuditoria
from nucleo.utilidades import ip_cliente

from .models import CORREO_SISTEMA, EventoAuditoria, Usuario

_contexto = contextvars.ContextVar("sirema_contexto_auditoria", default=None)

Accion = AccionAuditoria


class MiddlewareAuditoria:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = _contexto.set({"request": request})
        try:
            return self.get_response(request)
        finally:
            _contexto.reset(token)


def _request_actual():
    contexto = _contexto.get()
    return contexto["request"] if contexto else None


def usuario_sistema():
    usuario = Usuario.objects.filter(correo=CORREO_SISTEMA).first()
    if usuario is None:
        from .models import Rol

        rol = Rol.objects.get(nombre=Rol.BOMBERO)
        usuario = Usuario.objects.create(
            correo=CORREO_SISTEMA, rut="SISTEMA", nombre="Sistema", apellidos="SIREMA",
            rol=rol, activo=False, password="!",
        )
    return usuario


def _serializable(valor):
    if isinstance(valor, (datetime.datetime, datetime.date, datetime.time)):
        return valor.isoformat()
    if isinstance(valor, (decimal.Decimal, uuid.UUID)):
        return str(valor)
    if isinstance(valor, models.Model):
        return valor.pk if not isinstance(valor.pk, tuple) else list(valor.pk)
    if isinstance(valor, dict):
        return {k: _serializable(v) for k, v in valor.items()}
    if isinstance(valor, (list, tuple, set)):
        return [_serializable(v) for v in valor]
    return valor


def instantanea(objeto, campos=None, excluir=("password",)):
    """Diccionario con los valores actuales de un modelo, apto para JSONB."""
    datos = {}
    for campo in objeto._meta.concrete_fields:
        if campo.column is None:
            continue
        nombre = campo.attname
        if nombre in excluir or (campos and campo.name not in campos and nombre not in campos):
            continue
        datos[campo.column] = _serializable(getattr(objeto, nombre))
    return datos


def diferencias(anteriores, nuevos):
    """Deja solo las columnas que cambiaron."""
    claves = set(anteriores) | set(nuevos)
    cambiadas = {k for k in claves if anteriores.get(k) != nuevos.get(k)}
    return ({k: anteriores.get(k) for k in cambiadas}, {k: nuevos.get(k) for k in cambiadas})


def registrar(accion, entidad, id_registro, anteriores=None, nuevos=None, usuario=None, ip=None):
    request = _request_actual()
    if usuario is None and request is not None and getattr(request, "user", None) is not None \
            and request.user.is_authenticated:
        usuario = request.user
    if usuario is None:
        usuario = usuario_sistema()
    if ip is None:
        ip = ip_cliente(request)
    if isinstance(id_registro, (tuple, list)):
        id_registro = "-".join(str(p) for p in id_registro)
    return EventoAuditoria.objects.create(
        usuario=usuario,
        accion=accion,
        entidad_afectada=entidad,
        id_registro=str(id_registro),
        datos_anteriores=_serializable(anteriores) if anteriores else None,
        datos_nuevos=_serializable(nuevos) if nuevos else None,
        direccion_ip=ip or None,
    )
