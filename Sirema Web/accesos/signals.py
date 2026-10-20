"""Observador: los inicios y cierres de sesión quedan en la bitácora (RNF-09)."""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from nucleo.enums import AccionAuditoria
from nucleo.utilidades import ip_cliente

from . import auditoria
from .models import Usuario


@receiver(user_logged_in)
def inicio_sesion(sender, request, user, **kwargs):
    # RNF-02: registra la sesión como la única activa de este usuario.
    if request.session.session_key is None:
        request.session.save()
    Usuario.objects.filter(pk=user.pk).update(sesion_activa=request.session.session_key)
    auditoria.registrar(AccionAuditoria.ACCESO, "usuario", user.pk,
                        nuevos={"evento": "inicio_sesion"}, usuario=user, ip=ip_cliente(request))


@receiver(user_logged_out)
def cierre_sesion(sender, request, user, **kwargs):
    if user is not None and user.is_authenticated:
        Usuario.objects.filter(pk=user.pk).update(sesion_activa=None)
        auditoria.registrar(AccionAuditoria.ACCESO, "usuario", user.pk,
                            nuevos={"evento": "cierre_sesion"}, usuario=user, ip=ip_cliente(request))


@receiver(user_login_failed)
def intento_fallido(sender, credentials, request=None, **kwargs):
    correo = (credentials or {}).get("username") or (credentials or {}).get("correo")
    usuario = Usuario.objects.filter(correo__iexact=correo or "").first()
    if usuario is not None:
        auditoria.registrar(AccionAuditoria.ACCESO, "usuario", usuario.pk,
                            nuevos={"evento": "intento_fallido"}, usuario=usuario, ip=ip_cliente(request))
