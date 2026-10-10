"""
ProgramadorRevisiones (CU-C4 y CU-C5), ejecutado a diario por cron en el
contenedor sirema-scheduler mediante el comando generar_revisiones.

Es idempotente: la restricción única (id_asignacion, fecha_programada) impide
duplicar revisiones, de modo que puede repetirse y, si el servidor estuvo
apagado, recorre las fechas omitidas sin crear duplicados (curso 1.a).
"""
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
        """Crea las revisiones de una asignación hasta el horizonte. Devuelve las creadas."""
        material = asignacion.material
        if not asignacion.activa or material.estado != EstadoMaterial.ACTIVO:
            return []
        responsable = asignacion.usuario_responsable
        if responsable is None:
            log.warning("La asignación %s no tiene responsable; no se generan revisiones.", asignacion.pk)
            return []
        plan = asignacion.plan
        hasta = self.horizonte
        if asignacion.fecha_termino:
            # Curso 2.a: al alcanzar la fecha de término no se generan revisiones nuevas.
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
                        asignacion=asignacion, usuario_responsable=responsable, fecha_programada=fecha,
                        fecha_limite=fecha + timedelta(days=plan.dias_tolerancia),
                    )
                    auditoria.registrar(AccionAuditoria.ALTA, "revision", revision.pk, nuevos={
                        "id_asignacion": asignacion.pk, "fecha_programada": fecha,
                        "fecha_limite": revision.fecha_limite, "id_usuario_responsable": responsable.pk})
            except IntegrityError:
                continue  # otra ejecución la creó primero
            creadas.append(revision)
            notificaciones.notificar(
                responsable, TipoNotificacion.ASIGNACION,
                f"Nueva revisión asignada: {notificaciones.describir(revision)}, "
                f"fecha límite {revision.fecha_limite:%d-%m-%Y}.", revision, unica=True)
        return creadas

    def generar_revisiones(self):
        asignaciones = AsignacionPlan.objects.filter(activa=True).select_related(
            "plan", "material__cajonera__unidad", "usuario_responsable")
        return sum(len(self.generar_para(a)) for a in asignaciones)

    def marcar_vencidas(self):
        """Paso 4: las revisiones abiertas cuya fecha límite ya pasó quedan vencidas."""
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

    def emitir_avisos(self):
        """CU-C5: aviso 24 horas antes de la fecha límite y al vencer, con copia a la jefatura."""
        total = 0
        manana = self.fecha + timedelta(days=1)
        por_vencer = Revision.objects.completa().filter(
            estado__in=[EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO], fecha_limite=manana)
        for revision in por_vencer:
            mensaje = (f"Recordatorio: la revisión de {notificaciones.describir(revision)} vence mañana "
                       f"({revision.fecha_limite:%d-%m-%Y}).")
            total += bool(notificaciones.notificar(revision.usuario_responsable, TipoNotificacion.RECORDATORIO,
                                                   mensaje, revision, unica=True))
            total += len(notificaciones.notificar_jefatura(
                TipoNotificacion.RECORDATORIO, f"{mensaje} Responsable: {revision.usuario_responsable.nombre_corto}.",
                revision, unica=True, excluir=revision.usuario_responsable))

        for revision in Revision.objects.completa().filter(estado=EstadoRevision.VENCIDA):
            mensaje = (f"La revisión de {notificaciones.describir(revision)} venció el "
                       f"{revision.fecha_limite:%d-%m-%Y}.")
            total += bool(notificaciones.notificar(revision.usuario_responsable, TipoNotificacion.VENCIMIENTO,
                                                   mensaje, revision, unica=True))
            total += len(notificaciones.notificar_jefatura(
                TipoNotificacion.VENCIMIENTO, f"{mensaje} Responsable: {revision.usuario_responsable.nombre_corto}.",
                revision, unica=True, excluir=revision.usuario_responsable))
        return total

    def ejecutar(self):
        resumen = ResumenEjecucion()
        resumen.creadas = self.generar_revisiones()
        resumen.vencidas = self.marcar_vencidas()
        resumen.avisos = self.emitir_avisos()
        log.info("Programador %s: %s", self.fecha, resumen)
        return resumen
