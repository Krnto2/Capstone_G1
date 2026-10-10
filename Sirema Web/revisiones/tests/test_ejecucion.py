"""CP-08 Ejecución de revisiones, CP-11 Evidencia fotográfica y CP-12 Hallazgos."""
import json
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from accesos.models import EventoAuditoria
from nucleo.enums import EstadoRevision, TipoNotificacion
from nucleo.utilidades import hoy
from revisiones import services
from revisiones.models import Notificacion, PlanRevision, Revision

pytestmark = pytest.mark.django_db


def responder_todo(revision, usuario, presion="8"):
    puntos = {p.numero_orden: p for p in revision.plan.puntos.all()}
    services.registrar_resultado(revision, puntos[1], usuario, "conforme", "Sí")
    services.registrar_resultado(revision, puntos[2], usuario, "conforme", presion)


class TestCP08Ejecucion:
    def test_guarda_cada_respuesta_y_marca_en_curso(self, revision, bombero):
        punto = revision.plan.puntos.get(numero_orden=2)
        registro = services.registrar_resultado(revision, punto, bombero, "conforme", "8,5")
        revision.refresh_from_db()
        assert revision.estado == EstadoRevision.EN_CURSO and revision.fecha_hora_inicio
        assert registro.valor_registrado == "8.5"
        services.registrar_resultado(revision, punto, bombero, "falla", "12", "Válvula no regula")
        assert revision.resultados.count() == 1  # clave compuesta: una respuesta por punto

    def test_observacion_o_falla_exigen_comentario(self, revision, bombero):
        punto = revision.plan.puntos.get(numero_orden=1)
        with pytest.raises(services.ErrorRevision, match="comentario"):
            services.registrar_resultado(revision, punto, bombero, "observacion", "Sí", "")

    def test_valor_medido_debe_ser_numero(self, revision, bombero):
        with pytest.raises(services.ErrorRevision):
            services.registrar_resultado(revision, revision.plan.puntos.get(numero_orden=2), bombero, "conforme", "x")

    def test_punto_sugiere_falla_fuera_de_rango(self, plan):
        punto = plan.puntos.get(numero_orden=2)
        assert punto.evaluar("12") == "falla" and punto.evaluar("8") == "conforme"

    def test_no_finaliza_con_puntos_obligatorios_sin_responder(self, revision, bombero):
        with pytest.raises(services.ErrorRevision) as error:
            services.finalizar(revision, bombero)
        assert len(error.value.faltantes.puntos) == 2  # el tercero es opcional

    def test_resultado_global_y_bitacora(self, revision, bombero):
        responder_todo(revision, bombero)
        services.registrar_resultado(revision, revision.plan.puntos.get(numero_orden=3), bombero, "observacion",
                                     None, "Manguera reseca")
        revision = services.finalizar(revision, bombero, "Sin novedades mayores")
        assert revision.estado == EstadoRevision.REALIZADA and revision.resultado_global == "observacion"
        assert revision.usuario_ejecutor == bombero and revision.en_plazo
        assert EventoAuditoria.objects.filter(accion="revision", id_registro=str(revision.pk)).exists()

    def test_revision_finalizada_no_se_modifica(self, revision, bombero):
        responder_todo(revision, bombero)
        services.finalizar(revision, bombero)
        with pytest.raises(services.ErrorRevision, match="cerrada"):
            services.registrar_resultado(revision, revision.plan.puntos.first(), bombero, "conforme", "Sí")

    def test_solo_el_responsable_o_la_jefatura_ejecutan(self, revision, otro_bombero, jefatura):
        with pytest.raises(services.ErrorRevision, match="otro bombero"):
            services.iniciar(revision, otro_bombero)
        assert services.iniciar(revision, jefatura).estado == EstadoRevision.EN_CURSO

    def test_vencida_queda_realizada_fuera_de_plazo(self, revision, bombero):
        Revision.objects.filter(pk=revision.pk).update(estado=EstadoRevision.VENCIDA,
                                                       fecha_programada=hoy() - timedelta(days=5),
                                                       fecha_limite=hoy() - timedelta(days=4))
        revision.refresh_from_db()
        responder_todo(revision, bombero)
        assert services.finalizar(revision, bombero).en_plazo is False

    def test_api_json_de_autoguardado(self, client, revision, bombero):
        client.force_login(bombero)
        punto = revision.plan.puntos.get(numero_orden=2)
        url = reverse("revisiones:api_punto", args=[revision.pk, punto.pk])
        respuesta = client.post(url, json.dumps({"resultado": "falla", "valor": "12", "observacion": "No regula"}),
                                content_type="application/json")
        datos = respuesta.json()
        assert respuesta.status_code == 200 and datos["fuera_de_rango"] and datos["resumen"]["respondidos"] == 1
        error = client.post(url, json.dumps({"resultado": "falla", "valor": "12"}), content_type="application/json")
        assert error.status_code == 400 and "comentario" in error.json()["error"]


class TestCP11Fotografias:
    def test_plan_que_exige_foto_no_finaliza_sin_ella(self, revision, bombero, imagen):
        PlanRevision.objects.filter(pk=revision.plan.pk).update(exige_fotografia=True)
        revision.refresh_from_db()
        responder_todo(revision, bombero)
        with pytest.raises(services.ErrorRevision, match="fotografía"):
            services.finalizar(revision, bombero)
        foto = services.adjuntar_fotografia(revision, imagen(), bombero)
        assert len(foto.hash_sha256) == 64 and foto.usuario == bombero
        assert services.finalizar(revision, bombero).estado == EstadoRevision.REALIZADA

    def test_foto_de_punto_requiere_su_resultado_y_no_se_repite(self, revision, bombero, imagen):
        punto = revision.plan.puntos.get(numero_orden=1)
        with pytest.raises(services.ErrorRevision, match="Registre primero"):
            services.adjuntar_fotografia(revision, imagen(), bombero, punto=punto)
        services.registrar_resultado(revision, punto, bombero, "conforme", "Sí")
        services.adjuntar_fotografia(revision, imagen(color=(1, 2, 3)), bombero, punto=punto)
        with pytest.raises(services.ErrorRevision, match="ya fue cargada"):
            services.adjuntar_fotografia(revision, imagen(color=(1, 2, 3)), bombero, punto=punto)

    def test_anular_no_elimina_y_queda_en_bitacora(self, revision, bombero, jefatura, imagen):
        foto = services.adjuntar_fotografia(revision, imagen(), bombero)
        with pytest.raises(services.ErrorRevision):
            services.anular_fotografia(foto, "", jefatura)
        services.anular_fotografia(foto, "Foto de otro equipo", jefatura)
        foto.refresh_from_db()
        assert foto.anulada
        evento = EventoAuditoria.objects.get(entidad_afectada="fotografia", accion="baja")
        assert evento.datos_nuevos["motivo"] == "Foto de otro equipo" and evento.usuario == jefatura

    def test_entrega_protegida_de_fotografias(self, client, revision, bombero, imagen):
        foto = services.adjuntar_fotografia(revision, imagen(), bombero)
        url = reverse("revisiones:fotografia", args=[foto.pk])
        assert client.get(url).status_code == 302  # sin sesión
        client.force_login(bombero)
        respuesta = client.get(url)
        assert respuesta.status_code == 200 and respuesta["Content-Type"] == "image/jpeg"


class TestCP12Hallazgos:
    def test_falla_exige_hallazgo_y_notifica_a_jefatura(self, revision, bombero, jefatura):
        responder_todo(revision, bombero, presion="12")
        punto = revision.plan.puntos.get(numero_orden=2)
        services.registrar_resultado(revision, punto, bombero, "falla", "12", "Válvula no regula")
        with pytest.raises(services.ErrorRevision) as error:
            services.finalizar(revision, bombero)
        assert error.value.requiere_hallazgo
        revision = services.finalizar(revision, bombero, hallazgo={"descripcion": "Válvula de alivio dañada",
                                                                   "criticidad": "alta"})
        hallazgo = revision.hallazgos.get()
        assert revision.resultado_global == "falla" and hallazgo.estado == "abierto"
        assert Notificacion.objects.filter(usuario=jefatura, tipo=TipoNotificacion.HALLAZGO).exists()

    def test_solo_la_jefatura_cierra_registrando_la_accion(self, client, revision, bombero, jefatura):
        responder_todo(revision, bombero)
        services.registrar_resultado(revision, revision.plan.puntos.get(numero_orden=1), bombero, "falla", "No",
                                     "No enciende")
        revision = services.finalizar(revision, bombero, hallazgo={"descripcion": "No enciende", "criticidad": "media"})
        hallazgo = revision.hallazgos.get()
        url = reverse("revisiones:hallazgo", args=[hallazgo.pk])
        client.force_login(bombero)
        assert client.post(url, {"accion": "cerrar", "acciones": "x"}).status_code == 403
        client.force_login(jefatura)
        client.post(url, {"accion": "cerrar", "acciones": "Bujía reemplazada"})
        hallazgo.refresh_from_db()
        assert hallazgo.estado == "cerrado" and hallazgo.usuario_cierre == jefatura and hallazgo.fecha_cierre

    def test_notificacion_abierta_queda_leida(self, client, revision, bombero):
        aviso = Notificacion.objects.create(usuario=bombero, revision=revision, tipo="asignacion", mensaje="x")
        client.force_login(bombero)
        client.get(reverse("revisiones:notificacion", args=[aviso.pk]))
        aviso.refresh_from_db()
        assert aviso.leida and aviso.fecha_lectura <= timezone.now()
