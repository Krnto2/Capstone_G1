import logging
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction

from accesos import auditoria
from nucleo.enums import AccionAuditoria, EstadoMaterial, EstadoRevision, TipoNotificacion
from nucleo.utilidades import hoy

from . import notificaciones
from .models import AsignacionPlan, Revision

log = logging.getLogger("sirema.programador")

MAXIMO_ITERACIONES = 20000


@dataclass
class ResumenEjecucion:
    creadas: int = 0
    vencidas: int = 0
    avisos: int = 0

    def __str__(self):
        return f"{self.creadas} revisiones creadas, {self.vencidas} marcadas vencidas, {self.avisos} avisos emitidos"


class ProgramadorRevisiones:
    def __init__(self, fecha=None, anticipacion=None):
        self.fecha = fecha or hoy()
        self.anticipacion = settings.SIREMA_DIAS_ANTICIPACION if anticipacion is None else anticipacion

    @property
    def horizonte(self):
        return self.fecha + timedelta(days=self.anticipacion)

    def generar_para(self, asignacion):
        material = asignacion.material
        if not asignacion.activa or material.estado != EstadoMaterial.ACTIVO:
            return []
        responsables = list(asignacion.responsables.all())
        if not responsables:
            log.warning("La asignación %s no tiene responsables; no se generan revisiones.", asignacion.pk)
            return []
        plan = asignacion.plan
        hasta = self.horizonte
        if asignacion.fecha_termino:
            hasta = min(hasta, asignacion.fecha_termino)
        existentes = set(asignacion.revisiones.values_list("fecha_programada", flat=True))
        creadas = []
        for n in range(MAXIMO_ITERACIONES):
            fecha = plan.fecha_programada(asignacion.fecha_inicio, n)
            if fecha > hasta:
                break
            if fecha in existentes:
                continue
            try:
                with transaction.atomic():
                    revision = Revision.objects.create(
                        asignacion=asignacion, fecha_programada=fecha,
                        fecha_limite=fecha + timedelta(days=plan.dias_tolerancia),
                    )
                    revision.responsables.set(responsables)
                    auditoria.registrar(AccionAuditoria.ALTA, "revision", revision.pk, nuevos={
                        "id_asignacion": asignacion.pk, "fecha_programada": fecha,
                        "fecha_limite": revision.fecha_limite,
                        "id_usuarios_responsables": sorted(u.pk for u in responsables)})
            except IntegrityError:
                continue
            creadas.append(revision)
            for responsable in responsables:
                notificaciones.notificar(
                    responsable, TipoNotificacion.ASIGNACION,
                    f"Nueva revisión asignada: {notificaciones.describir(revision)}, "
                    f"fecha límite {revision.fecha_limite:%d-%m-%Y}.", revision, unica=True)
        return creadas

    def generar_revisiones(self):
        asignaciones = AsignacionPlan.objects.filter(activa=True).select_related(
            "plan", "material__cajonera__unidad").prefetch_related("responsables")
        return sum(len(self.generar_para(a)) for a in asignaciones)

    def marcar_vencidas(self):
        vencidas = Revision.objects.filter(estado__in=[EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO],
                                           fecha_limite__lt=self.fecha)
        total = 0
        for revision in vencidas:
            with transaction.atomic():
                anterior = revision.estado
                revision.estado = EstadoRevision.VENCIDA
                revision.save(update_fields=["estado"])
                auditoria.registrar(AccionAuditoria.MODIFICACION, "revision", revision.pk, {"estado": anterior},
                                    {"estado": EstadoRevision.VENCIDA})
            total += 1
        return total

    @staticmethod
    def _avisar(revision, tipo, mensaje):
        responsables = list(revision.responsables.all())
        total = sum(bool(notificaciones.notificar(u, tipo, mensaje, revision, unica=True)) for u in responsables)
        titulo = "Responsable" if len(responsables) == 1 else "Responsables"
        return total + len(notificaciones.notificar_jefatura(
            tipo, f"{mensaje} {titulo}: {revision.responsables_cortos}.", revision, unica=True, excluir=responsables))

    def emitir_avisos(self):
        total = 0
        manana = self.fecha + timedelta(days=1)
        por_vencer = Revision.objects.completa().filter(
            estado__in=[EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO], fecha_limite=manana)
        for revision in por_vencer:
            mensaje = (f"Recordatorio: la revisión de {notificaciones.describir(revision)} vence mañana "
                       f"({revision.fecha_limite:%d-%m-%Y}).")
            total += self._avisar(revision, TipoNotificacion.RECORDATORIO, mensaje)

        for revision in Revision.objects.completa().filter(estado=EstadoRevision.VENCIDA):
            mensaje = (f"La revisión de {notificaciones.describir(revision)} venció el "
                       f"{revision.fecha_limite:%d-%m-%Y}.")
            total += self._avisar(revision, TipoNotificacion.VENCIMIENTO, mensaje)
        return total

    def ejecutar(self):
        resumen = ResumenEjecucion()
        resumen.creadas = self.generar_revisiones()
        resumen.vencidas = self.marcar_vencidas()
        resumen.avisos = self.emitir_avisos()
        log.info("Programador %s: %s", self.fecha, resumen)
        return resumen
