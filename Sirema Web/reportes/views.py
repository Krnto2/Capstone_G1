from django.http import Http404, HttpResponse
from django.views import View
from django.views.generic import TemplateView

from accesos.permisos import PermisoRequeridoMixin
from inventario.models import Categoria, Unidad
from nucleo.utilidades import hoy, nombre_mes, sumar_meses

from . import exportacion
from .indicadores import Filtros, ServicioReportes


def opciones_periodo(cantidad=13):
    actual = hoy().replace(day=1)
    meses = [sumar_meses(actual, -i) for i in range(cantidad)]
    return [(f"{m.year:04d}-{m.month:02d}", nombre_mes(m.year, m.month)) for m in meses]


class FiltrosMixin:
    def contexto_filtros(self):
        filtros = Filtros.desde_parametros(self.request.GET)
        periodos = opciones_periodo()
        if filtros.periodo not in dict(periodos):
            periodos.insert(0, (filtros.periodo, nombre_mes(filtros.anio, filtros.mes)))
        return filtros, {"filtros": filtros, "periodos": periodos, "unidades": Unidad.objects.all(),
                         "categorias": Categoria.objects.all(), "parametros": filtros.como_parametros()}


class PanelView(PermisoRequeridoMixin, FiltrosMixin, TemplateView):
    """CU-C14 Consultar panel de cumplimiento (pantalla D1)."""

    permiso_requerido = "panel.consultar"
    template_name = "reportes/panel.html"

    def get_context_data(self, **kwargs):
        filtros, contexto = self.contexto_filtros()
        contexto["ind"] = ServicioReportes(filtros).cumplimiento()
        return super().get_context_data(**contexto, **kwargs)


class ReportesView(PermisoRequeridoMixin, FiltrosMixin, TemplateView):
    """Detalle del período con exportación (CU-C15)."""

    permiso_requerido = "reporte.exportar"
    template_name = "reportes/reportes.html"

    def get_context_data(self, **kwargs):
        filtros, contexto = self.contexto_filtros()
        servicio = ServicioReportes(filtros)
        contexto["ind"] = servicio.cumplimiento()
        contexto["revisiones"] = servicio.detalle()
        return super().get_context_data(**contexto, **kwargs)


class ExportarView(PermisoRequeridoMixin, View):
    """CU-C15 Exportar reporte de cumplimiento en PDF, XLSX o CSV."""

    permiso_requerido = "reporte.exportar"
    tipos = {
        "csv": "text/csv; charset=utf-8",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pdf": "application/pdf",
    }

    def get(self, request, formato):
        if formato not in self.tipos:
            raise Http404
        filtros = Filtros.desde_parametros(request.GET)
        servicio = ServicioReportes(filtros)
        indicadores, revisiones = servicio.cumplimiento(), list(servicio.detalle())
        if formato == "csv":
            contenido = exportacion.exportar_csv(indicadores, revisiones)
        elif formato == "xlsx":
            contenido = exportacion.exportar_xlsx(indicadores, revisiones)
        else:
            contenido, es_pdf = exportacion.exportar_pdf(indicadores, revisiones)
            if not es_pdf:
                return HttpResponse(contenido)
        respuesta = HttpResponse(contenido, content_type=self.tipos[formato])
        respuesta["Content-Disposition"] = f'attachment; filename="{exportacion.nombre_archivo(filtros, formato)}"'
        return respuesta
