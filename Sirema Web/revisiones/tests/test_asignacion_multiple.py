"""Asignación múltiple: varios planes y elementos a la vez, y tareas compartidas entre bomberos."""
from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from inventario import services as inventario
from nucleo.enums import EstadoRevision, TipoNotificacion
from nucleo.utilidades import hoy
from revisiones import services
from revisiones.models import AsignacionPlan, Notificacion, PlanRevision, PuntoControl, Revision
from revisiones.programador import ProgramadorRevisiones

pytestmark = pytest.mark.django_db


@pytest.fixture
def otro_plan(db):
    plan = PlanRevision.objects.create(nombre="Plan mensual", frecuencia_valor=1, frecuencia_unidad="mes",
                                       exige_fotografia=False)
    PuntoControl.objects.create(plan=plan, numero_orden=1, descripcion="Limpieza", tipo_dato="seleccion")
    return plan


@pytest.fixture
def otro_material(catalogo, jefatura):
    return inventario.registrar_material({
        "codigo_institucional": "8C-0999", "nombre": "Generador", "categoria": catalogo["motores"],
        "cajonera": catalogo["cabina"], "tipo": "unitario", "cantidad": 1,
    }, jefatura)


@pytest.fixture
def compartida(plan, material, bombero, otro_bombero, jefatura):
    asignacion, revisiones = services.asignar_plan(plan, material, [bombero, otro_bombero], hoy(), jefatura)
    return revisiones[0]


class TestLote:
    def test_varias_tareas_a_un_bombero(self, plan, otro_plan, material, otro_material, bombero, jefatura):
        resultado = services.asignar_en_lote([plan, otro_plan], [material, otro_material], [bombero], hoy(), jefatura)
        assert len(resultado.asignaciones) == 4 and not resultado.omitidas
        assert bombero.asignaciones_responsable.count() == 4
        assert Revision.objects.filter(responsables=bombero).count() >= 4

    def test_una_tarea_a_varios_bomberos(self, plan, material, bombero, otro_bombero, jefatura):
        resultado = services.asignar_en_lote([plan], [material], [bombero, otro_bombero], hoy(), jefatura)
        asignacion = resultado.asignaciones[0]
        assert AsignacionPlan.objects.count() == 1
        assert set(asignacion.responsables.all()) == {bombero, otro_bombero}
        for revision in asignacion.revisiones.all():
            assert set(revision.responsables.all()) == {bombero, otro_bombero}
        for usuario in (bombero, otro_bombero):
            assert Notificacion.objects.filter(usuario=usuario, tipo=TipoNotificacion.ASIGNACION).exists()

    def test_omite_lo_vigente_y_crea_lo_demas(self, plan, otro_plan, material, bombero, jefatura):
        services.asignar_plan(plan, material, [bombero], hoy(), jefatura)
        resultado = services.asignar_en_lote([plan, otro_plan], [material], [bombero], hoy(), jefatura)
        assert [a.plan for a in resultado.asignaciones] == [otro_plan]
        assert resultado.omitidas == [(plan, material)]

    def test_todo_vigente_avisa(self, plan, material, bombero, jefatura):
        services.asignar_plan(plan, material, [bombero], hoy(), jefatura)
        with pytest.raises(ValidationError, match="ya está vigente"):
            services.asignar_en_lote([plan], [material], [bombero], hoy(), jefatura)

    def test_si_una_falla_no_queda_ninguna(self, plan, material, otro_material, bombero, jefatura):
        otro_material.dar_de_baja("prueba", jefatura)
        with pytest.raises(ValidationError, match="activos"):
            services.asignar_en_lote([plan], [material, otro_material], [bombero], hoy(), jefatura)
        assert not AsignacionPlan.objects.exists() and not Revision.objects.exists()

    def test_exige_responsables_que_puedan_ejecutar(self, plan, material, bombero, jefatura):
        with pytest.raises(ValidationError, match="al menos un bombero"):
            services.asignar_plan(plan, material, [], hoy(), jefatura)
        bombero.desactivar()
        with pytest.raises(ValidationError, match="no puede ejecutar"):
            services.asignar_plan(plan, material, [bombero], hoy(), jefatura)


class TestTareaCompartida:
    def test_todos_la_ven_y_cualquiera_la_ejecuta(self, compartida, bombero, otro_bombero, jefatura, client):
        for usuario in (bombero, otro_bombero):
            client.force_login(usuario)
            pagina = client.get(reverse("revisiones:mis_revisiones")).content.decode()
            assert "Compartida:" in pagina and reverse("revisiones:ejecutar", args=[compartida.pk]) in pagina
            assert client.get(reverse("revisiones:ejecutar", args=[compartida.pk])).status_code == 200

    def test_quien_no_es_responsable_no_la_ejecuta(self, compartida, administrador):
        assert not services.puede_ejecutar(compartida, administrador)

    def test_basta_que_uno_la_finalice(self, compartida, plan, bombero, otro_bombero):
        for punto, valor in zip(plan.puntos.all(), ("Sí", "8", None)):
            services.registrar_resultado(compartida, punto, otro_bombero, "conforme", valor)
        services.finalizar(compartida, otro_bombero)
        compartida.refresh_from_db()
        assert compartida.estado == EstadoRevision.REALIZADA and compartida.usuario_ejecutor == otro_bombero
        with pytest.raises(ValidationError, match="ya fue cerrada"):
            services.registrar_resultado(compartida, plan.puntos.first(), bombero, "conforme", "Sí")
        assert compartida not in Revision.objects.pendientes_de(bombero)

    def test_realizada_no_se_duplica_en_mis_revisiones(self, compartida, bombero, otro_bombero, client):
        Revision.objects.filter(pk=compartida.pk).update(estado=EstadoRevision.REALIZADA, usuario_ejecutor=bombero)
        client.force_login(bombero)
        contexto = client.get(reverse("revisiones:mis_revisiones") + "?ver=realizadas").context
        assert [r.pk for r in contexto["revisiones"]] == [compartida.pk]

    def test_el_programador_mantiene_a_todos(self, compartida, bombero, otro_bombero):
        siguientes = ProgramadorRevisiones(fecha=hoy() + timedelta(weeks=1)).generar_para(compartida.asignacion)
        assert siguientes
        assert set(siguientes[0].responsables.all()) == {bombero, otro_bombero}

    def test_los_avisos_llegan_a_todos_sin_duplicar(self, compartida, bombero, otro_bombero, jefatura):
        Revision.objects.filter(pk=compartida.pk).update(fecha_limite=hoy() + timedelta(days=1))
        programador = ProgramadorRevisiones()
        programador.emitir_avisos()
        programador.emitir_avisos()
        filtro = {"tipo": TipoNotificacion.RECORDATORIO, "revision": compartida}
        assert Notificacion.objects.filter(usuario=bombero, **filtro).count() == 1
        assert Notificacion.objects.filter(usuario=otro_bombero, **filtro).count() == 1
        assert "Responsables: M. Rivas, J. Soto." in Notificacion.objects.get(usuario=jefatura, **filtro).mensaje

    def test_cuenta_una_sola_vez_en_los_reportes(self, compartida):
        from reportes.indicadores import Filtros, ServicioReportes

        filtros = Filtros(compartida.fecha_limite.year, compartida.fecha_limite.month)
        assert ServicioReportes(filtros).revisiones_periodo().filter(pk=compartida.pk).count() == 1


class TestCambiarResponsables:
    def test_alcanza_a_las_abiertas_y_avisa_solo_a_quien_se_suma(self, revision, bombero, otro_bombero, jefatura):
        Notificacion.objects.all().delete()
        services.cambiar_responsables(revision.asignacion, [bombero, otro_bombero], jefatura)
        assert set(revision.asignacion.responsables.all()) == {bombero, otro_bombero}
        assert set(revision.responsables.all()) == {bombero, otro_bombero}
        assert Notificacion.objects.filter(usuario=otro_bombero).count() == 1
        assert not Notificacion.objects.filter(usuario=bombero).exists()

    def test_no_cambia_revisiones_cerradas(self, revision, bombero, otro_bombero, jefatura):
        Revision.objects.filter(pk=revision.pk).update(estado=EstadoRevision.REALIZADA)
        services.cambiar_responsables(revision.asignacion, [otro_bombero], jefatura)
        assert list(revision.responsables.all()) == [bombero]

    def test_reasignar_una_revision_a_varios(self, revision, bombero, otro_bombero, jefatura):
        services.reasignar(revision, [bombero, otro_bombero], jefatura)
        assert set(revision.responsables.all()) == {bombero, otro_bombero}
        assert list(revision.asignacion.responsables.all()) == [bombero]  # solo esta revisión

    def test_una_version_nueva_del_plan_conserva_a_todos(self, compartida, plan, bombero, otro_bombero, jefatura):
        services.registrar_resultado(compartida, plan.puntos.first(), bombero, "conforme", "Sí")
        datos = {"nombre": plan.nombre, "frecuencia_valor": 1, "frecuencia_unidad": "semana", "dias_tolerancia": 0,
                 "exige_fotografia": False}
        puntos = [{"descripcion": "Otro", "tipo_dato": "seleccion", "obligatorio": True, "exige_fotografia": False}]
        nuevo, es_nueva = services.guardar_plan(plan, datos, puntos, jefatura)
        assert es_nueva
        assert set(nuevo.asignaciones.get().responsables.all()) == {bombero, otro_bombero}


class TestVistas:
    def _datos(self, planes, materiales, responsables):
        return {"planes": [p.pk for p in planes], "materiales": [m.pk for m in materiales],
                "responsables": [u.pk for u in responsables], "fecha_inicio": hoy().isoformat()}

    def test_la_jefatura_asigna_en_lote(self, client, jefatura, plan, otro_plan, material, otro_material, bombero,
                                        otro_bombero):
        client.force_login(jefatura)
        respuesta = client.post(reverse("revisiones:asignacion_crear"),
                                self._datos([plan, otro_plan], [material, otro_material], [bombero, otro_bombero]))
        assert respuesta.status_code == 302
        assert AsignacionPlan.objects.count() == 4

    def test_avisa_lo_que_ya_estaba_vigente(self, client, jefatura, plan, otro_plan, material, bombero):
        services.asignar_plan(plan, material, [bombero], hoy(), jefatura)
        client.force_login(jefatura)
        respuesta = client.post(reverse("revisiones:asignacion_crear"),
                                self._datos([plan, otro_plan], [material], [bombero]), follow=True)
        texto = respuesta.content.decode()
        assert "1 asignación creada" in texto and "Ya estaban vigentes" in texto

    def test_exige_las_tres_selecciones(self, client, jefatura):
        client.force_login(jefatura)
        texto = client.post(reverse("revisiones:asignacion_crear"), {"fecha_inicio": hoy().isoformat()}).content.decode()
        for mensaje in ("al menos un elemento", "al menos un plan", "al menos un bombero"):
            assert mensaje in texto

    def test_precarga_desde_el_plan_y_desde_la_ficha(self, client, jefatura, plan, material):
        client.force_login(jefatura)
        form = client.get(reverse("revisiones:asignacion_crear"),
                          {"plan": plan.pk, "material": material.pk}).context["form"]
        assert form["planes"].value() == [str(plan.pk)] and form["materiales"].value() == [str(material.pk)]

    def test_un_bombero_no_asigna(self, client, bombero):
        client.force_login(bombero)
        assert client.get(reverse("revisiones:asignacion_crear")).status_code == 403

    def test_la_jefatura_suma_un_bombero_a_una_asignacion(self, client, jefatura, revision, bombero, otro_bombero):
        client.force_login(jefatura)
        url = reverse("revisiones:asignacion_responsables", args=[revision.asignacion.pk])
        assert client.get(url).status_code == 200
        assert client.post(url, {"responsables": [bombero.pk, otro_bombero.pk]}).status_code == 302
        assert set(revision.responsables.all()) == {bombero, otro_bombero}

    def test_reasignar_en_pantalla(self, client, jefatura, revision, otro_bombero):
        client.force_login(jefatura)
        url = reverse("revisiones:reasignar", args=[revision.pk])
        assert client.get(url).status_code == 200
        assert client.post(url, {"responsables": [otro_bombero.pk]}).status_code == 302
        assert list(revision.responsables.all()) == [otro_bombero]
