"""
API JSON de la ejecución de revisiones (DAS 4.3.3, docs/openapi.yaml).

Durante una revisión el navegador guarda cada punto con fetch y sube las
fotografías en solicitudes multipart. El resto del sistema usa páginas HTML.
"""
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from accesos.permisos import permiso_requerido

from . import services
from .models import PuntoControl, Revision


def _error(mensaje, estado=400, **extra):
    return JsonResponse({"ok": False, "error": mensaje, **extra}, status=estado)


def _revision(pk):
    return get_object_or_404(Revision.objects.select_related("asignacion__plan"), pk=pk)


def _estado(revision):
    faltan = services.faltantes(revision)
    return {"faltantes": faltan.como_dict(), "resumen": services.resumen(revision)}


@require_POST
@permiso_requerido("revision.ejecutar")
def registrar_punto(request, pk, punto_id):
    revision = _revision(pk)
    punto = get_object_or_404(PuntoControl, pk=punto_id)
    try:
        datos = json.loads(request.body or b"{}")
    except (ValueError, UnicodeDecodeError):
        return _error("Solicitud no válida.")
    try:
        registro = services.registrar_resultado(revision, punto, request.user, datos.get("resultado"),
                                                datos.get("valor"), datos.get("observacion"))
    except services.ErrorRevision as error:
        return _error(error.messages[0])
    return JsonResponse({
        "ok": True,
        "punto": punto.pk,
        "resultado": registro.resultado,
        "valor": registro.valor_registrado,
        "fuera_de_rango": punto.fuera_de_rango(registro.valor_registrado),
        "guardado": timezone.localtime(registro.fecha_hora_registro).strftime("%H:%M"),
        **_estado(revision),
    })


@require_POST
@permiso_requerido("revision.ejecutar")
def subir_fotografia(request, pk):
    revision = _revision(pk)
    archivo = request.FILES.get("archivo")
    if archivo is None:
        return _error("Adjunte una fotografía.")
    punto = None
    if request.POST.get("punto"):
        punto = get_object_or_404(PuntoControl, pk=request.POST["punto"])
    try:
        foto = services.adjuntar_fotografia(revision, archivo, request.user, punto=punto,
                                            descripcion=request.POST.get("descripcion"))
    except services.ErrorRevision as error:
        return _error(error.messages[0])
    return JsonResponse({
        "ok": True,
        "id": str(foto.pk),
        "url": reverse("revisiones:fotografia", args=[foto.pk]),
        "punto": foto.punto_id,
        "hash": foto.hash_sha256,
        **_estado(revision),
    }, status=201)


@require_GET
@permiso_requerido("revision.ejecutar")
def estado_revision(request, pk):
    revision = _revision(pk)
    if not services.puede_ver(revision, request.user):
        return _error("Sin permiso.", 403)
    return JsonResponse({"ok": True, "estado": revision.estado, **_estado(revision)})
