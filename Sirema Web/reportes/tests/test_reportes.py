"""CP-09 Panel de cumplimiento y CP-10 Historial y reportes."""
from datetime import datetime, time, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from nucleo.enums import EstadoRevision
from nucleo.utilidades import hoy
from reportes.indicadores import Filtros, ServicioReportes
from revisiones.models import Hallazgo, Revision

pytestmark = pytest.mark.django_db


def _revision(asignacion, responsable, dias_atras, estado, termino_dias_atras=None):
    programada = hoy() - timedelta(days=dias_atras)
    revision = Revision.objects.create(asignacion=asignacion, usuario_responsable=responsable,
                                       fecha_programada=programada, fecha_limite=programada + timedelta(days=1),
                                       estado=estado)
    if termino_dias_atras is not None:
        termino = datetime.combine(hoy() - timedelta(days=termino_dias_atras), time(10), timezone.get_current_timezone())
        Revision.objects.filter(pk=revision.pk).update(fecha_hora_inicio=termino, fecha_hora_termino=termino,
                                                       usuario_ejecutor=responsable, resultado_global="conforme")
    return revision


class TestCP09Panel:
    def test_porcentaje_de_cumplimiento(self, asignacion, bombero):
        # Se usan días dentro del mes actual para que todas caigan en el período.
        base = min(hoy().day - 1, 8)
        if base < 4:
            pytest.skip("Muy temprano en el mes para armar el escenario")
        _revision(asignacion, bombero, base, EstadoRevision.REALIZADA, termino_dias_atras=base)      # en plazo
        _revision(asignacion, bombero, base - 1, EstadoRevision.REALIZADA, termino_dias_atras=base - 3)  # fuera
        _revision(asignacion, bombero, base - 2, EstadoRevision.VENCIDA)                              # vencida
        _revision(asignacion, bombero, -3, EstadoRevision.PENDIENTE)                                  # aún en plazo
        ind = ServicioReportes(Filtros(hoy().year, hoy().month)).cumplimiento()
        assert ind.exigibles == 3 and ind.en_plazo == 1 and ind.fuera_de_plazo == 1
        assert ind.porcentaje == pytest.approx(33.3, abs=0.1)
        assert len(ind.vencidas) == 1

    def test_elementos_sin_plan_y_hallazgos_abiertos(self, material, revision, bombero):
        Hallazgo.objects.create(revision=revision, descripcion="Falla", criticidad="alta")
        ind = ServicioReportes(Filtros(hoy().year, hoy().month)).cumplimiento()
        assert ind.total_activos == 1 and ind.sin_plan == 0
        assert len(ind.hallazgos_abiertos) == 1 and ind.hallazgos_alta == 1

    def test_panel_solo_para_jefatura(self, client, bombero, jefatura, asignacion):
        client.force_login(bombero)
        assert client.get(reverse("reportes:panel")).status_code == 403
        client.force_login(jefatura)
        respuesta = client.get(reverse("reportes:panel"), {"periodo": f"{hoy():%Y-%m}"})
        assert respuesta.status_code == 200 and "ind" in respuesta.context


class TestCP10Reportes:
    @pytest.mark.parametrize("formato,tipo", [("xlsx", "spreadsheetml"), ("csv", "text/csv")])
    def test_exporta_reporte(self, client, jefatura, revision, formato, tipo):
        client.force_login(jefatura)
        respuesta = client.get(reverse("reportes:exportar", args=[formato]), {"periodo": f"{hoy():%Y-%m}"})
        assert respuesta.status_code == 200 and tipo in respuesta["Content-Type"]
        assert "attachment" in respuesta["Content-Disposition"]

    def test_exporta_pdf_o_vista_imprimible(self, client, jefatura, revision):
        client.force_login(jefatura)
        respuesta = client.get(reverse("reportes:exportar", args=["pdf"]))
        assert respuesta.status_code == 200
        assert respuesta["Content-Type"] in ("application/pdf", "text/html; charset=utf-8")

    def test_historial_del_elemento_desde_lo_mas_reciente(self, client, material, catalogo, bombero, revision):
        material.trasladar(catalogo["caj2"], bombero, "Reorganización")
        client.force_login(bombero)
        eventos = client.get(reverse("inventario:detalle", args=[material.pk])).context["eventos"]
        assert len(eventos) >= 2
        assert eventos == sorted(eventos, key=lambda e: e["fecha"], reverse=True)
