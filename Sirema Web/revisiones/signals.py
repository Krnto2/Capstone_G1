"""
Observadores del módulo de revisiones.

- Baja de un elemento (señal del inventario): cierra sus asignaciones y deja
  no realizadas sus revisiones abiertas (RF-03).
- Proveedor de la ficha de material: aporta revisiones y hallazgos al
  historial del elemento (CU-B6).
"""
from datetime import datetime, time

from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from accesos import auditoria
from inventario.signals import material_dado_de_baja
from nucleo.enums import AccionAuditoria, EstadoRevision

from .models import AsignacionPlan, Hallazgo, Revision, RevisionQuerySet


@receiver(material_dado_de_baja)
def cerrar_por_baja(sender, material, usuario, **kwargs):
    for asignacion in AsignacionPlan.objects.filter(material=material, activa=True):
        asignacion.cerrar()
        auditoria.registrar(AccionAuditoria.BAJA, "asignacion_plan", asignacion.pk, {"activa": True},
                            {"activa": False, "motivo": "baja del elemento"}, usuario=usuario)
    for revision in Revision.objects.filter(asignacion__material=material, estado__in=RevisionQuerySet.ABIERTAS):
        anterior = revision.estado
        revision.estado = EstadoRevision.NO_REALIZADA
        revision.save(update_fields=["estado"])
        auditoria.registrar(AccionAuditoria.MODIFICACION, "revision", revision.pk, {"estado": anterior},
                            {"estado": EstadoRevision.NO_REALIZADA, "motivo": "baja del elemento"}, usuario=usuario)


class ProveedorFichaMaterial:
    TONOS = {"conforme": "conforme", "observacion": "observacion", "falla": "falla"}

    def eventos(self, material):
        eventos = []
        revisiones = Revision.objects.filter(asignacion__material=material).exclude(
            estado__in=[EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO]).select_related(
            "asignacion__plan", "usuario_ejecutor", "usuario_responsable")
        for r in revisiones:
            if r.estado == EstadoRevision.REALIZADA:
                plazo = "" if r.en_plazo else " · fuera de plazo"
                eventos.append({"fecha": r.fecha_hora_termino, "icono": "bi-clipboard-check",
                                "titulo": f"Revisión {r.get_resultado_global_display().lower()} · {r.asignacion.plan}",
                                "detalle": f"Programada {r.fecha_programada:%d-%m-%Y}{plazo}",
                                "usuario": r.usuario_ejecutor.nombre_corto if r.usuario_ejecutor else "",
                                "tono": self.TONOS.get(r.resultado_global, "neutro"),
                                "url": reverse("revisiones:detalle", args=[r.pk])})
            else:
                eventos.append({"fecha": _fecha_hora(r.fecha_limite), "icono": "bi-clipboard-x",
                                "titulo": f"Revisión {r.get_estado_display().lower()} · {r.asignacion.plan}",
                                "detalle": f"Fecha límite {r.fecha_limite:%d-%m-%Y}",
                                "usuario": r.usuario_responsable.nombre_corto, "tono": "falla",
                                "url": reverse("revisiones:detalle", args=[r.pk])})
        for h in Hallazgo.objects.filter(revision__asignacion__material=material).select_related("usuario_cierre"):
            eventos.append({"fecha": h.fecha_apertura, "icono": "bi-exclamation-octagon",
                            "titulo": f"Hallazgo de criticidad {h.get_criticidad_display().lower()}",
                            "detalle": h.descripcion, "usuario": "", "tono": "falla",
                            "url": reverse("revisiones:hallazgo", args=[h.pk])})
            if h.fecha_cierre:
                eventos.append({"fecha": h.fecha_cierre, "icono": "bi-check2-square", "titulo": "Hallazgo cerrado",
                                "detalle": h.acciones or "",
                                "usuario": h.usuario_cierre.nombre_corto if h.usuario_cierre else "",
                                "tono": "conforme", "url": reverse("revisiones:hallazgo", args=[h.pk])})
        return eventos

    def secciones(self, material):
        return [{
            "plantilla": "revisiones/_ficha_material.html",
            "contexto": {
                "asignaciones": AsignacionPlan.objects.filter(material=material, activa=True).select_related(
                    "plan", "usuario_responsable"),
                "abiertas": Revision.objects.completa().filter(asignacion__material=material).abiertas()
                .por_urgencia(),
                "hallazgos": Hallazgo.objects.filter(revision__asignacion__material=material)
                .exclude(estado="cerrado"),
            },
        }]


def _fecha_hora(fecha):
    return datetime.combine(fecha, time(23, 59), timezone.get_current_timezone())
