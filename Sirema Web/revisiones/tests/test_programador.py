"""CP-07 Planes de revisión y programador de tareas; avisos de CP-09."""
from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command

from nucleo.enums import EstadoRevision, TipoNotificacion
from nucleo.utilidades import hoy
from revisiones import services
from revisiones.models import AsignacionPlan, Notificacion, PlanRevision, Revision
from revisiones.programador import ProgramadorRevisiones

pytestmark = pytest.mark.django_db


class TestCP07Programador:
    def test_genera_revisiones_hasta_el_horizonte_sin_duplicar(self, asignacion):
        programador = ProgramadorRevisiones(fecha=hoy(), anticipacion=14)
        creadas = programador.generar_revisiones()
        assert creadas == 3  # hoy, +7 y +14 días (plan semanal)
        assert programador.generar_revisiones() == 0  # idempotente
        primera = asignacion.revisiones.order_by("fecha_programada").first()
        assert primera.fecha_limite == primera.fecha_programada + timedelta(days=1)

    def test_recupera_fechas_omitidas_si_el_servidor_estuvo_apagado(self, asignacion):
        AsignacionPlan.objects.filter(pk=asignacion.pk).update(fecha_inicio=hoy() - timedelta(weeks=3))
        asignacion.refresh_from_db()
        creadas = ProgramadorRevisiones(fecha=hoy(), anticipacion=0).generar_para(asignacion)
        assert [r.fecha_programada for r in creadas] == [hoy() - timedelta(weeks=n) for n in (3, 2, 1, 0)]

    def test_respeta_la_fecha_de_termino(self, asignacion):
        AsignacionPlan.objects.filter(pk=asignacion.pk).update(fecha_termino=hoy() + timedelta(days=3))
        asignacion.refresh_from_db()
        assert len(ProgramadorRevisiones(anticipacion=30).generar_para(asignacion)) == 1

    def test_marca_vencidas_y_emite_avisos_con_copia_a_jefatura(self, revision, jefatura, bombero):
        Revision.objects.filter(pk=revision.pk).update(fecha_programada=hoy() - timedelta(days=3),
                                                       fecha_limite=hoy() - timedelta(days=2))
        programador = ProgramadorRevisiones(anticipacion=0)
        assert programador.marcar_vencidas() == 1
        programador.emitir_avisos()
        revision.refresh_from_db()
        assert revision.estado == EstadoRevision.VENCIDA
        assert Notificacion.objects.filter(usuario=bombero, tipo=TipoNotificacion.VENCIMIENTO).count() == 1
        assert Notificacion.objects.filter(usuario=jefatura, tipo=TipoNotificacion.VENCIMIENTO).count() == 1
        programador.emitir_avisos()  # no repite avisos
        assert Notificacion.objects.filter(tipo=TipoNotificacion.VENCIMIENTO).count() == 2

    def test_aviso_24_horas_antes(self, revision, bombero):
        Revision.objects.filter(pk=revision.pk).update(fecha_limite=hoy() + timedelta(days=1))
        ProgramadorRevisiones().emitir_avisos()
        assert Notificacion.objects.filter(usuario=bombero, tipo=TipoNotificacion.RECORDATORIO).exists()

    def test_comando_generar_revisiones(self, asignacion, capsys):
        call_command("generar_revisiones")
        assert "revisiones creadas" in capsys.readouterr().out
        assert asignacion.revisiones.exists()


class TestCP07Planes:
    PUNTOS = [{"descripcion": "Nivel de aceite", "tipo_dato": "booleano", "obligatorio": True,
               "exige_fotografia": False}]

    def test_plan_exige_al_menos_un_punto(self, jefatura):
        with pytest.raises(ValidationError):
            services.guardar_plan(None, {"nombre": "Vacío", "frecuencia_valor": 1, "frecuencia_unidad": "mes",
                                         "dias_tolerancia": 0, "exige_fotografia": False}, [], jefatura)

    def test_modificar_plan_con_ejecuciones_crea_version_nueva(self, revision, plan, bombero, jefatura):
        services.registrar_resultado(revision, plan.puntos.get(numero_orden=1), bombero, "conforme", "Sí")
        datos = {"nombre": plan.nombre, "frecuencia_valor": 1, "frecuencia_unidad": "semana", "dias_tolerancia": 2,
                 "exige_fotografia": False}
        nuevo, es_version = services.guardar_plan(plan, datos, self.PUNTOS, jefatura)
        plan.refresh_from_db()
        assert es_version and nuevo.version == 2 and not plan.activo
        assert plan.puntos.count() == 3  # la versión histórica no cambia
        assert AsignacionPlan.objects.filter(plan=nuevo, activa=True).count() == 1
        assert not AsignacionPlan.objects.filter(plan=plan, activa=True).exists()

    def test_modificar_plan_sin_ejecuciones_lo_actualiza(self, plan, jefatura):
        datos = {"nombre": plan.nombre, "frecuencia_valor": 2, "frecuencia_unidad": "semana", "dias_tolerancia": 0,
                 "exige_fotografia": True}
        mismo, es_version = services.guardar_plan(plan, datos, self.PUNTOS, jefatura)
        assert mismo.pk == plan.pk and not es_version and mismo.puntos.count() == 1
        assert PlanRevision.objects.count() == 1

    def test_asignar_plan_valida_y_notifica(self, plan, material, bombero, jefatura):
        asignacion, creadas = services.asignar_plan(plan, material, bombero, hoy(), jefatura)
        assert asignacion.activa and creadas
        assert Notificacion.objects.filter(usuario=bombero, tipo=TipoNotificacion.ASIGNACION).exists()
        with pytest.raises(ValidationError, match="vigente"):
            services.asignar_plan(plan, material, bombero, hoy(), jefatura)

    def test_no_asigna_planes_a_elementos_dados_de_baja(self, plan, material, bombero, jefatura):
        material.dar_de_baja("prueba", jefatura)
        with pytest.raises(ValidationError, match="activos"):
            services.asignar_plan(plan, material, bombero, hoy(), jefatura)
