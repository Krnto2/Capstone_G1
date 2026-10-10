from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, ProtectedError, Q, RestrictedError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from accesos import auditoria
from accesos.permisos import PermisoRequeridoMixin
from nucleo.enums import AccionAuditoria, EstadoMaterial

from . import importacion, registro, services
from .forms import (FiltroMaterial, FormularioBaja, FormularioCajonera, FormularioCategoria, FormularioImportacion,
                    FormularioMaterial, FormularioMovimiento, FormularioUnidad)
from .models import Cajonera, Categoria, Material, Unidad

# ------------------------------------------------------------- Material ----


class MaterialListaView(PermisoRequeridoMixin, ListView):
    """CU-B4 Buscar material."""

    permiso_requerido = "material.consultar"
    template_name = "inventario/material_lista.html"
    context_object_name = "materiales"
    paginate_by = 25

    def get_queryset(self):
        self.filtro = FiltroMaterial(self.request.GET or {"estado": "activo"})
        return self.filtro.filtrar(Material.objects.con_ubicacion())

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["filtro"] = self.filtro
        contexto["total_activos"] = Material.objects.activos().count()
        q = self.request.GET.get("q", "").strip()
        contexto["busqueda_corta"] = len(q) == 1
        return contexto


class MaterialDetalleView(PermisoRequeridoMixin, DetailView):
    """Ficha del elemento y CU-B6 Consultar historial (lo más reciente primero)."""

    permiso_requerido = "material.consultar"
    template_name = "inventario/material_detalle.html"
    context_object_name = "material"
    queryset = Material.objects.con_ubicacion()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        material = self.object
        eventos = []
        for mov in material.movimientos.select_related("cajonera_origen__unidad", "cajonera_destino__unidad",
                                                       "usuario"):
            if mov.cajonera_origen_id:
                titulo = f"Traslado a {mov.cajonera_destino}"
                detalle = f"Desde {mov.cajonera_origen}" + (f" · {mov.motivo}" if mov.motivo else "")
            else:
                titulo = f"Alta en el inventario · {mov.cajonera_destino}"
                detalle = mov.motivo or ""
            eventos.append({"fecha": mov.fecha_hora, "icono": "bi-arrow-left-right", "titulo": titulo,
                            "detalle": detalle, "usuario": mov.usuario.nombre_corto, "tono": "neutro"})
        baja = getattr(material, "baja", None)
        if baja:
            eventos.append({"fecha": baja.fecha, "icono": "bi-archive", "titulo": "Dado de baja",
                            "detalle": baja.motivo + (f" · destino: {baja.destino_final}" if baja.destino_final else ""),
                            "usuario": baja.usuario.nombre_corto, "tono": "falla"})
        eventos.extend(registro.eventos_historial(material))
        eventos.sort(key=lambda e: e["fecha"], reverse=True)
        contexto["eventos"] = eventos
        contexto["secciones"] = registro.secciones_ficha(material)
        contexto["baja"] = baja
        return contexto


class MaterialCrearView(PermisoRequeridoMixin, View):
    """CU-B1 Registrar material."""

    permiso_requerido = "material.registrar"
    template_name = "inventario/material_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": FormularioMaterial(), "titulo": "Registrar material"})

    def post(self, request):
        form = FormularioMaterial(request.POST)
        if form.is_valid():
            try:
                material = services.registrar_material(form.cleaned_data, request.user)
            except ValidationError as error:
                _errores_a_formulario(form, error)
            else:
                messages.success(request, f"«{material}» quedó registrado en {material.ubicacion}.")
                if "otro" in request.POST:
                    return redirect("inventario:crear")
                return redirect("inventario:detalle", pk=material.pk)
        return render(request, self.template_name, {"form": form, "titulo": "Registrar material"})


class MaterialEditarView(PermisoRequeridoMixin, View):
    """CU-B2 Modificar ficha de material."""

    permiso_requerido = "material.modificar"
    template_name = "inventario/material_form.html"

    def _material(self, pk):
        material = get_object_or_404(Material.objects.con_ubicacion(), pk=pk)
        if not material.activo:
            messages.error(self.request, "Un elemento dado de baja no se puede modificar.")
        return material

    def get(self, request, pk):
        material = self._material(pk)
        if not material.activo:
            return redirect("inventario:detalle", pk=pk)
        return render(request, self.template_name, {"form": FormularioMaterial(instance=material),
                                                    "material": material, "titulo": "Modificar ficha"})

    def post(self, request, pk):
        material = self._material(pk)
        if not material.activo:
            return redirect("inventario:detalle", pk=pk)
        form = FormularioMaterial(request.POST, instance=Material.objects.get(pk=pk))
        if form.is_valid():
            try:
                services.modificar_material(material, form.cleaned_data, request.user)
            except ValidationError as error:
                _errores_a_formulario(form, error)
            else:
                messages.success(request, "La ficha fue actualizada.")
                return redirect("inventario:detalle", pk=pk)
        return render(request, self.template_name, {"form": form, "material": material,
                                                    "titulo": "Modificar ficha"})


class MaterialBajaView(PermisoRequeridoMixin, View):
    """CU-B3 Dar de baja material (incluye CU-B4: se llega desde la búsqueda)."""

    permiso_requerido = "material.dar_de_baja"
    template_name = "inventario/material_baja.html"

    def get(self, request, pk):
        material = get_object_or_404(Material.objects.con_ubicacion(), pk=pk)
        return render(request, self.template_name, {"material": material, "form": FormularioBaja()})

    def post(self, request, pk):
        material = get_object_or_404(Material.objects.con_ubicacion(), pk=pk)
        form = FormularioBaja(request.POST)
        if form.is_valid():
            try:
                material.dar_de_baja(form.cleaned_data["motivo"], request.user, form.cleaned_data["destino_final"])
            except ValidationError as error:
                form.add_error(None, error)
            else:
                messages.success(request, f"«{material}» fue dado de baja.")
                return redirect("inventario:detalle", pk=pk)
        return render(request, self.template_name, {"material": material, "form": form})


class MovimientoView(PermisoRequeridoMixin, View):
    """CU-B5 Registrar movimiento de material."""

    permiso_requerido = "movimiento.registrar"
    template_name = "inventario/movimiento_form.html"

    def get(self, request, pk):
        material = get_object_or_404(Material.objects.con_ubicacion(), pk=pk)
        if not material.activo:
            messages.error(request, "No se pueden mover elementos dados de baja.")
            return redirect("inventario:detalle", pk=pk)
        return render(request, self.template_name, {"material": material,
                                                    "form": FormularioMovimiento(material=material)})

    def post(self, request, pk):
        material = get_object_or_404(Material.objects.con_ubicacion(), pk=pk)
        form = FormularioMovimiento(request.POST, material=material)
        if form.is_valid():
            try:
                material.trasladar(form.cleaned_data["cajonera_destino"], request.user, form.cleaned_data["motivo"])
            except ValidationError as error:
                form.add_error(None, error)
            else:
                messages.success(request, f"«{material}» ahora está en {material.ubicacion}.")
                return redirect("inventario:detalle", pk=pk)
        return render(request, self.template_name, {"material": material, "form": form})


class ImportarView(PermisoRequeridoMixin, View):
    """CU-B1, curso alternativo 3.a: carga masiva desde planilla."""

    permiso_requerido = "material.registrar"
    template_name = "inventario/importar.html"

    def get(self, request):
        return render(request, self.template_name, {"form": FormularioImportacion(),
                                                    "columnas": importacion.COLUMNAS,
                                                    "obligatorias": importacion.OBLIGATORIAS})

    def post(self, request):
        form = FormularioImportacion(request.POST, request.FILES)
        resultado = None
        if form.is_valid():
            try:
                resultado = importacion.importar_planilla(form.cleaned_data["archivo"], request.user)
            except ValidationError as error:
                form.add_error("archivo", error)
        return render(request, self.template_name, {"form": form, "resultado": resultado,
                                                    "columnas": importacion.COLUMNAS,
                                                    "obligatorias": importacion.OBLIGATORIAS})


class PlantillaImportacionView(PermisoRequeridoMixin, View):
    permiso_requerido = "material.registrar"

    def get(self, request):
        respuesta = HttpResponse(importacion.plantilla_csv(), content_type="text/csv; charset=utf-8")
        respuesta["Content-Disposition"] = 'attachment; filename="plantilla_material_sirema.csv"'
        return respuesta


def _errores_a_formulario(form, error):
    if hasattr(error, "error_dict"):
        for campo, errores in error.message_dict.items():
            form.add_error(campo if campo in form.fields else None, errores)
    else:
        form.add_error(None, error)


# ------------------------------------------------------------ Catálogos ----

class CatalogoMixin(PermisoRequeridoMixin):
    """CU-B7 y CU-B8: formularios simples con auditoría."""

    permiso_requerido = "catalogo.administrar"
    form_class = None
    modelo = None
    entidad = ""
    template_name = "inventario/catalogo_form.html"
    titulo = ""
    volver = ""

    def objeto(self, pk):
        return get_object_or_404(self.modelo, pk=pk) if pk else None

    def initial(self):
        return {}

    def get(self, request, pk=None):
        objeto = self.objeto(pk)
        form = self.form_class(instance=objeto, initial=self.initial())
        return render(request, self.template_name, self.contexto(form, objeto))

    def post(self, request, pk=None):
        objeto = self.objeto(pk)
        anteriores = auditoria.instantanea(objeto) if objeto else None
        form = self.form_class(request.POST, instance=objeto)
        if form.is_valid():
            with transaction.atomic():
                guardado = form.save()
                if anteriores:
                    antes, despues = auditoria.diferencias(anteriores, auditoria.instantanea(guardado))
                    if despues:
                        auditoria.registrar(AccionAuditoria.MODIFICACION, self.entidad, guardado.pk, antes, despues)
                else:
                    auditoria.registrar(AccionAuditoria.ALTA, self.entidad, guardado.pk,
                                        nuevos=auditoria.instantanea(guardado))
            messages.success(request, f"{self.titulo_corto} «{guardado}» guardada.")
            return redirect(self.volver)
        return render(request, self.template_name, self.contexto(form, objeto))

    titulo_corto = ""

    def contexto(self, form, objeto):
        titulo = f"Editar {self.titulo_corto.lower()}" if objeto else self.titulo
        return {"form": form, "objeto": objeto, "titulo": titulo, "volver": reverse(self.volver)}


class UnidadesView(PermisoRequeridoMixin, TemplateView):
    """CU-B7 Administrar unidades y cajoneras."""

    permiso_requerido = "catalogo.administrar"
    template_name = "inventario/unidad_lista.html"

    def get_context_data(self, **kwargs):
        unidades = Unidad.objects.prefetch_related("cajoneras").annotate(
            n_elementos=Count("cajoneras__materiales", filter=Q(cajoneras__materiales__estado=EstadoMaterial.ACTIVO)))
        conteo = dict(Cajonera.objects.annotate(
            n=Count("materiales", filter=Q(materiales__estado=EstadoMaterial.ACTIVO))).values_list("pk", "n"))
        return super().get_context_data(unidades=unidades, conteo=conteo, **kwargs)


class UnidadFormView(CatalogoMixin, View):
    form_class = FormularioUnidad
    modelo = Unidad
    entidad = "unidad"
    titulo = "Nueva unidad"
    titulo_corto = "Unidad"
    volver = "inventario:unidades"


class CajoneraFormView(CatalogoMixin, View):
    form_class = FormularioCajonera
    modelo = Cajonera
    entidad = "cajonera"
    titulo = "Nueva cajonera"
    titulo_corto = "Cajonera"
    volver = "inventario:unidades"

    def initial(self):
        return {"unidad": self.request.GET.get("unidad")}


class CategoriasView(PermisoRequeridoMixin, ListView):
    """CU-B8 Administrar categorías."""

    permiso_requerido = "catalogo.administrar"
    template_name = "inventario/categoria_lista.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.annotate(n_elementos=Count("materiales"))


class CategoriaFormView(CatalogoMixin, View):
    form_class = FormularioCategoria
    modelo = Categoria
    entidad = "categoria"
    titulo = "Nueva categoría"
    titulo_corto = "Categoría"
    volver = "inventario:categorias"


class EliminarCatalogoView(PermisoRequeridoMixin, View):
    """Elimina una unidad, cajonera o categoría solo si no tiene elementos (RF-05, RF-06)."""

    permiso_requerido = "catalogo.administrar"
    modelos = {"unidad": (Unidad, "inventario:unidades"), "cajonera": (Cajonera, "inventario:unidades"),
               "categoria": (Categoria, "inventario:categorias")}

    def post(self, request, entidad, pk):
        if entidad not in self.modelos:
            raise Http404
        modelo, volver = self.modelos[entidad]
        objeto = get_object_or_404(modelo, pk=pk)
        if self._tiene_elementos(entidad, objeto):
            messages.error(request, f"«{objeto}» tiene elementos asociados y no se puede eliminar.")
            return redirect(volver)
        try:
            with transaction.atomic():
                datos = auditoria.instantanea(objeto)
                if entidad == "unidad":
                    objeto.cajoneras.all().delete()
                objeto.delete()
                auditoria.registrar(AccionAuditoria.BAJA, entidad, pk, anteriores=datos)
        except (ProtectedError, RestrictedError):
            messages.error(request, f"«{objeto}» conserva historial de movimientos y no se puede eliminar."
                           + (" Puede desactivar la unidad." if entidad != "categoria" else ""))
        else:
            messages.success(request, f"«{objeto}» fue eliminado.")
        return redirect(volver)

    @staticmethod
    def _tiene_elementos(entidad, objeto):
        if entidad == "unidad":
            return Material.objects.filter(cajonera__unidad=objeto).exists()
        return objeto.materiales.exists()
