from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from accesos.permisos import PermisoRequeridoMixin, verificar
from inventario.models import Material
from nucleo.almacenamiento import ErrorAlmacenamiento, ServicioAlmacenamiento
from nucleo.enums import EstadoHallazgo, EstadoRevision, ResultadoControl

from . import services
from .forms import (FiltroHallazgos, FiltroRevisiones, FormsetPuntos, FormularioAsignacion, FormularioCierreHallazgo,
                    FormularioFinalizar, FormularioMotivo, FormularioPlan, FormularioReasignar)
from .models import AsignacionPlan, Fotografia, Hallazgo, Notificacion, PlanRevision, Revision

# ------------------------------------------------------------ Revisiones ----


class MisRevisionesView(PermisoRequeridoMixin, TemplateView):
    """CU-C6 Consultar revisiones pendientes (pantalla M2)."""

    permiso_requerido = "revision.ejecutar"
    template_name = "revisiones/mis_revisiones.html"

    def get_context_data(self, **kwargs):
        usuario = self.request.user
        base = Revision.objects.completa()
        pendientes = base.filter(usuario_responsable=usuario,
                                 estado__in=[EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO]).por_urgencia()
        vencidas = base.filter(usuario_responsable=usuario, estado=EstadoRevision.VENCIDA).por_urgencia()
        realizadas = base.filter(Q(usuario_ejecutor=usuario) | Q(usuario_responsable=usuario),
                                 estado=EstadoRevision.REALIZADA).order_by("-fecha_hora_termino")[:30]
        pestana = self.request.GET.get("ver", "pendientes")
        if pestana not in ("pendientes", "vencidas", "realizadas"):
            pestana = "pendientes"
        listas = {"pendientes": pendientes, "vencidas": vencidas, "realizadas": realizadas}
        return super().get_context_data(
            pestana=pestana, revisiones=listas[pestana], n_pendientes=pendientes.count(),
            n_vencidas=vencidas.count(), **kwargs)


class RevisionListaView(PermisoRequeridoMixin, ListView):
    """Todas las revisiones, para la jefatura."""

    permiso_requerido = "revision.supervisar"
    template_name = "revisiones/revision_lista.html"
    context_object_name = "revisiones"
    paginate_by = 30

    def get_queryset(self):
        self.filtro = FiltroRevisiones(self.request.GET or None)
        revisiones = Revision.objects.completa().order_by("-fecha_limite", "-id")
        if self.filtro.is_valid():
            datos = self.filtro.cleaned_data
            if datos["q"] and len(datos["q"].strip()) >= 2:
                q = datos["q"].strip()
                revisiones = revisiones.filter(Q(asignacion__material__nombre__icontains=q)
                                               | Q(asignacion__material__codigo_institucional__icontains=q))
            if datos["estado"]:
                revisiones = revisiones.filter(estado=datos["estado"])
            if datos["unidad"]:
                revisiones = revisiones.filter(asignacion__material__cajonera__unidad=datos["unidad"])
            if datos["responsable"]:
                revisiones = revisiones.filter(usuario_responsable=datos["responsable"])
            if datos["desde"]:
                revisiones = revisiones.filter(fecha_limite__gte=datos["desde"])
            if datos["hasta"]:
                revisiones = revisiones.filter(fecha_limite__lte=datos["hasta"])
        return revisiones

    def get_context_data(self, **kwargs):
        return super().get_context_data(filtro=self.filtro, **kwargs)


class RevisionDetalleView(DetailView):
    template_name = "revisiones/revision_detalle.html"
    context_object_name = "revision"

    def get_queryset(self):
        return Revision.objects.completa()

    def get_object(self, queryset=None):
        revision = super().get_object(queryset)
        if not services.puede_ver(revision, self.request.user):
            raise PermissionDenied
        return revision

    def get_context_data(self, **kwargs):
        revision = self.object
        resultados = {r.punto_id: r for r in revision.resultados.all()}
        fotos = list(revision.fotografias.select_related("usuario"))
        puntos = [{"punto": p, "resultado": resultados.get(p.pk), "fotos": [f for f in fotos if f.punto_id == p.pk]}
                  for p in revision.plan.puntos.all()]
        return super().get_context_data(
            puntos=puntos, fotos_generales=[f for f in fotos if f.punto_id is None],
            hallazgos=revision.hallazgos.all(), puede_ejecutar=services.puede_ejecutar(revision, self.request.user)
            and revision.ejecutable, **kwargs)


class EjecutarView(PermisoRequeridoMixin, View):
    """CU-C7 Ejecutar revisión (pantalla M3)."""

    permiso_requerido = "revision.ejecutar"
    template_name = "revisiones/ejecutar.html"

    def get(self, request, pk):
        revision = get_object_or_404(Revision.objects.completa(), pk=pk)
        if not revision.ejecutable:
            messages.info(request, "Esta revisión ya fue cerrada.")
            return redirect("revisiones:detalle", pk=pk)
        try:
            services.iniciar(revision, request.user)
        except services.ErrorRevision as error:
            messages.error(request, error.messages[0])
            return redirect("revisiones:mis_revisiones")
        resultados = {r.punto_id: r for r in revision.resultados.all()}
        fotos = list(revision.fotografias.filter(anulada=False))
        puntos = []
        for punto in revision.plan.puntos.all():
            resultado = resultados.get(punto.pk)
            puntos.append({"punto": punto, "resultado": resultado,
                           "fotos": [f for f in fotos if f.punto_id == punto.pk],
                           "fuera_de_rango": bool(resultado and punto.fuera_de_rango(resultado.valor_registrado))})
        return render(request, self.template_name, {
            "revision": revision, "puntos": puntos, "fotos_generales": [f for f in fotos if f.punto_id is None],
            "faltantes": services.faltantes(revision), "resumen": services.resumen(revision),
        })


class FinalizarView(PermisoRequeridoMixin, View):
    """CU-C7 pasos 5 a 7 y CU-C12 Registrar hallazgo (pantalla M4)."""

    permiso_requerido = "revision.ejecutar"
    template_name = "revisiones/finalizar.html"

    def _preparar(self, request, pk):
        revision = get_object_or_404(Revision.objects.completa(), pk=pk)
        if not revision.ejecutable:
            messages.info(request, "Esta revisión ya fue cerrada.")
            return revision, redirect("revisiones:detalle", pk=pk)
        if not services.puede_ejecutar(revision, request.user):
            raise PermissionDenied
        faltan = services.faltantes(revision)
        if faltan.hay:
            messages.error(request, f"{faltan.texto}. Complete la lista antes de finalizar.")
            return revision, redirect("revisiones:ejecutar", pk=pk)
        return revision, None

    def _contexto(self, revision, form):
        resumen = services.resumen(revision)
        return {"revision": revision, "form": form, "resumen": resumen,
                "es_falla": resumen["resultado_global"] == ResultadoControl.FALLA}

    def get(self, request, pk):
        revision, salida = self._preparar(request, pk)
        if salida:
            return salida
        es_falla = services.resumen(revision)["resultado_global"] == ResultadoControl.FALLA
        return render(request, self.template_name,
                      self._contexto(revision, FormularioFinalizar(requiere_hallazgo=es_falla)))

    def post(self, request, pk):
        revision, salida = self._preparar(request, pk)
        if salida:
            return salida
        es_falla = services.resumen(revision)["resultado_global"] == ResultadoControl.FALLA
        form = FormularioFinalizar(request.POST, requiere_hallazgo=es_falla)
        if form.is_valid():
            datos = form.cleaned_data
            hallazgo = {"descripcion": datos["descripcion"], "criticidad": datos["criticidad"]} if es_falla else None
            try:
                revision = services.finalizar(revision, request.user, datos["observaciones"], hallazgo)
            except services.ErrorRevision as error:
                form.add_error(None, error.messages[0])
            else:
                texto = "Revisión finalizada"
                if revision.resultado_global == ResultadoControl.FALLA:
                    texto += ". El hallazgo quedó abierto y la jefatura fue notificada"
                if revision.en_plazo is False:
                    texto += ". Quedó registrada fuera de plazo"
                messages.success(request, texto + ".")
                return redirect("revisiones:detalle", pk=revision.pk)
        return render(request, self.template_name, self._contexto(revision, form))


class ReasignarView(PermisoRequeridoMixin, View):
    permiso_requerido = "revision.supervisar"
    template_name = "revisiones/reasignar.html"

    def get(self, request, pk):
        revision = get_object_or_404(Revision.objects.completa(), pk=pk)
        return render(request, self.template_name, {"revision": revision, "form": FormularioReasignar(
            initial={"responsable": revision.usuario_responsable_id})})

    def post(self, request, pk):
        revision = get_object_or_404(Revision.objects.completa(), pk=pk)
        form = FormularioReasignar(request.POST)
        if form.is_valid():
            try:
                services.reasignar(revision, form.cleaned_data["responsable"], request.user)
            except services.ErrorRevision as error:
                form.add_error(None, error.messages[0])
            else:
                messages.success(request, f"Revisión reasignada a {revision.usuario_responsable.nombre_completo}.")
                return redirect("revisiones:detalle", pk=pk)
        return render(request, self.template_name, {"revision": revision, "form": form})


# ----------------------------------------------------------- Fotografías ----

class FotografiaView(View):
    """Entrega protegida: Django verifica el permiso y Nginx sirve el archivo (X-Accel-Redirect)."""

    def get(self, request, pk):
        foto = get_object_or_404(Fotografia.objects.select_related("revision"), pk=pk)
        if not services.puede_ver(foto.revision, request.user):
            raise PermissionDenied
        if settings.SIREMA_USAR_X_ACCEL:
            respuesta = HttpResponse(content_type=foto.tipo_mime)
            respuesta["X-Accel-Redirect"] = settings.SIREMA_X_ACCEL_PREFIJO + foto.ruta_almacenamiento
        else:
            try:
                ruta = ServicioAlmacenamiento().ruta_absoluta(foto.ruta_almacenamiento)
                respuesta = FileResponse(open(ruta, "rb"), content_type=foto.tipo_mime)
            except (OSError, ErrorAlmacenamiento) as error:
                raise Http404("Archivo no disponible.") from error
        respuesta["Cache-Control"] = "private, max-age=3600"
        return respuesta


class AnularFotografiaView(PermisoRequeridoMixin, View):
    """CU-C11 Anular fotografía."""

    permiso_requerido = "fotografia.anular"
    template_name = "revisiones/anular_foto.html"

    def get(self, request, pk):
        foto = get_object_or_404(Fotografia.objects.select_related("revision", "punto", "usuario"), pk=pk)
        return render(request, self.template_name, {"foto": foto, "form": FormularioMotivo(),
                                                    "integra": ServicioAlmacenamiento().verificar(foto)})

    def post(self, request, pk):
        foto = get_object_or_404(Fotografia.objects.select_related("revision", "punto", "usuario"), pk=pk)
        form = FormularioMotivo(request.POST)
        if form.is_valid():
            try:
                services.anular_fotografia(foto, form.cleaned_data["motivo"], request.user)
            except services.ErrorRevision as error:
                form.add_error(None, error.messages[0])
            else:
                messages.success(request, "La fotografía fue anulada. El motivo quedó en la bitácora.")
                return redirect("revisiones:detalle", pk=foto.revision_id)
        return render(request, self.template_name, {"foto": foto, "form": form,
                                                    "integra": ServicioAlmacenamiento().verificar(foto)})


# ---------------------------------------------------------------- Planes ----

class PlanListaView(PermisoRequeridoMixin, ListView):
    permiso_requerido = "plan.administrar"
    template_name = "revisiones/plan_lista.html"
    context_object_name = "planes"

    def get_queryset(self):
        planes = PlanRevision.objects.annotate(
            n_puntos=Count("puntos", distinct=True),
            n_asignaciones=Count("asignaciones", filter=Q(asignaciones__activa=True), distinct=True))
        if self.request.GET.get("ver") != "todos":
            planes = planes.filter(activo=True)
        return planes


class PlanFormView(PermisoRequeridoMixin, View):
    """CU-C1 Definir plan de revisión, que incluye CU-C2 Definir puntos de control."""

    permiso_requerido = "plan.administrar"
    template_name = "revisiones/plan_form.html"

    def _plan(self, pk):
        return get_object_or_404(PlanRevision, pk=pk, activo=True) if pk else None

    def get(self, request, pk=None):
        plan = self._plan(pk)
        inicial = [{"descripcion": p.descripcion, "tipo_dato": p.tipo_dato, "unidad_medida": p.unidad_medida,
                    "valor_minimo": p.valor_minimo, "valor_maximo": p.valor_maximo, "obligatorio": p.obligatorio,
                    "exige_fotografia": p.exige_fotografia, "ORDER": p.numero_orden}
                   for p in plan.puntos.all()] if plan else None
        return render(request, self.template_name, {
            "plan": plan, "form": FormularioPlan(instance=plan), "formset": FormsetPuntos(prefix="puntos",
                                                                                        initial=inicial),
            "versiona": plan is not None and services.tiene_ejecuciones(plan),
        })

    def post(self, request, pk=None):
        plan = self._plan(pk)
        form = FormularioPlan(request.POST, instance=PlanRevision.objects.get(pk=plan.pk) if plan else None)
        formset = FormsetPuntos(request.POST, prefix="puntos")
        if form.is_valid() and formset.is_valid():
            try:
                guardado, es_nueva = services.guardar_plan(plan, form.cleaned_data, formset.puntos(), request.user)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                if es_nueva:
                    messages.success(request, f"Se creó la versión {guardado.version} del plan. Las revisiones "
                                              "ya ejecutadas conservan la versión anterior.")
                else:
                    messages.success(request, f"Plan «{guardado}» guardado.")
                return redirect("revisiones:plan", pk=guardado.pk)
        return render(request, self.template_name, {
            "plan": plan, "form": form, "formset": formset,
            "versiona": plan is not None and services.tiene_ejecuciones(plan),
        })


class PlanDetalleView(PermisoRequeridoMixin, DetailView):
    permiso_requerido = "plan.administrar"
    template_name = "revisiones/plan_detalle.html"
    context_object_name = "plan"
    model = PlanRevision

    def get_context_data(self, **kwargs):
        plan = self.object
        return super().get_context_data(
            asignaciones=plan.asignaciones.filter(activa=True).select_related(
                "material__cajonera__unidad", "usuario_responsable"),
            versiones=PlanRevision.objects.filter(nombre__iexact=plan.nombre).exclude(pk=plan.pk),
            **kwargs)


class PlanDesactivarView(PermisoRequeridoMixin, View):
    permiso_requerido = "plan.administrar"

    def post(self, request, pk):
        plan = get_object_or_404(PlanRevision, pk=pk, activo=True)
        cerradas = services.desactivar_plan(plan, request.user)
        messages.success(request, f"Plan desactivado. Se cerraron {cerradas} asignaciones vigentes.")
        return redirect("revisiones:planes")


# --------------------------------------------------------- Asignaciones ----

class AsignacionListaView(PermisoRequeridoMixin, ListView):
    permiso_requerido = "asignacion.administrar"
    template_name = "revisiones/asignacion_lista.html"
    context_object_name = "asignaciones"
    paginate_by = 30

    def get_queryset(self):
        asignaciones = AsignacionPlan.objects.select_related("plan", "material__cajonera__unidad",
                                                             "usuario_responsable")
        if self.request.GET.get("ver") != "todas":
            asignaciones = asignaciones.filter(activa=True)
        q = self.request.GET.get("q", "").strip()
        if len(q) >= 2:
            asignaciones = asignaciones.filter(Q(material__nombre__icontains=q)
                                               | Q(material__codigo_institucional__icontains=q)
                                               | Q(plan__nombre__icontains=q))
        return asignaciones

    def get_context_data(self, **kwargs):
        sin_plan = Material.objects.activos().exclude(asignaciones__activa=True).count()
        return super().get_context_data(sin_plan=sin_plan, **kwargs)


class AsignacionCrearView(PermisoRequeridoMixin, View):
    """CU-C3 Asignar plan a material (incluye CU-B4 Buscar material)."""

    permiso_requerido = "asignacion.administrar"
    template_name = "revisiones/asignacion_form.html"

    def _contexto(self, request, form, material=None):
        q = request.GET.get("q", "").strip()
        resultados = []
        if len(q) >= 2:
            resultados = list(Material.objects.activos().con_ubicacion().buscar(q)[:20])
        if material is None and request.GET.get("material"):
            material = Material.objects.activos().con_ubicacion().filter(pk=request.GET["material"]).first()
        planes_vigentes = []
        if material:
            planes_vigentes = list(material.asignaciones.filter(activa=True).select_related("plan"))
        return {"form": form, "q": q, "resultados": resultados, "material": material,
                "planes_vigentes": planes_vigentes, "busqueda_corta": len(q) == 1}

    def get(self, request):
        form = FormularioAsignacion(initial={"plan": request.GET.get("plan")})
        return render(request, self.template_name, self._contexto(request, form))

    def post(self, request):
        form = FormularioAsignacion(request.POST)
        material = Material.objects.con_ubicacion().filter(pk=request.POST.get("material") or 0).first()
        if material is None:
            form.add_error(None, "Busque y seleccione el elemento al que asignará el plan.")
        if form.is_valid() and material is not None:
            datos = form.cleaned_data
            try:
                asignacion, creadas = services.asignar_plan(datos["plan"], material, datos["responsable"],
                                                            datos["fecha_inicio"], request.user,
                                                            datos.get("fecha_termino"))
            except ValidationError as error:
                form.add_error(None, error)
            else:
                limite = datos["fecha_inicio"] + timedelta(days=datos["plan"].dias_tolerancia)
                messages.success(request, f"Plan asignado a {material}. Primera revisión: "
                                          f"{datos['fecha_inicio']:%d-%m-%Y} (límite {limite:%d-%m-%Y}). "
                                          f"Se notificó a {datos['responsable'].nombre_completo}.")
                return redirect("revisiones:asignaciones")
        return render(request, self.template_name, self._contexto(request, form, material))


class AsignacionCerrarView(PermisoRequeridoMixin, View):
    permiso_requerido = "asignacion.administrar"

    def post(self, request, pk):
        asignacion = get_object_or_404(AsignacionPlan, pk=pk)
        try:
            services.cerrar_asignacion(asignacion, request.user)
        except ValidationError as error:
            messages.error(request, error.messages[0])
        else:
            messages.success(request, "La asignación fue cerrada. No se generarán nuevas revisiones.")
        return redirect(request.POST.get("siguiente") or "revisiones:asignaciones")


# ------------------------------------------------------------- Hallazgos ----

class HallazgoListaView(PermisoRequeridoMixin, ListView):
    permiso_requerido = "hallazgo.gestionar"
    template_name = "revisiones/hallazgo_lista.html"
    context_object_name = "hallazgos"
    paginate_by = 30

    def get_queryset(self):
        self.filtro = FiltroHallazgos(self.request.GET or None)
        hallazgos = Hallazgo.objects.select_related("revision__asignacion__material__cajonera__unidad",
                                                    "revision__usuario_ejecutor", "usuario_cierre")
        estado, criticidad = "abiertos", ""
        if self.filtro.is_valid():
            estado = self.filtro.cleaned_data["estado"] or "abiertos"
            criticidad = self.filtro.cleaned_data["criticidad"]
        if estado == "abiertos":
            hallazgos = hallazgos.exclude(estado=EstadoHallazgo.CERRADO)
        elif estado != "todos":
            hallazgos = hallazgos.filter(estado=estado)
        if criticidad:
            hallazgos = hallazgos.filter(criticidad=criticidad)
        return hallazgos

    def get_context_data(self, **kwargs):
        return super().get_context_data(filtro=self.filtro, **kwargs)


class HallazgoDetalleView(View):
    """CU-C13 Cerrar hallazgo."""

    template_name = "revisiones/hallazgo_detalle.html"

    def _hallazgo(self, request, pk):
        hallazgo = get_object_or_404(Hallazgo.objects.select_related(
            "revision__asignacion__material__cajonera__unidad", "revision__asignacion__plan",
            "revision__usuario_ejecutor", "usuario_cierre"), pk=pk)
        if not (verificar(request.user, "hallazgo.gestionar") or services.puede_ver(hallazgo.revision, request.user)):
            raise PermissionDenied
        return hallazgo

    def get(self, request, pk):
        hallazgo = self._hallazgo(request, pk)
        return render(request, self.template_name, {"hallazgo": hallazgo, "form": FormularioCierreHallazgo()})

    def post(self, request, pk):
        hallazgo = self._hallazgo(request, pk)
        if not request.user.tiene_permiso("hallazgo.gestionar"):
            raise PermissionDenied
        form = FormularioCierreHallazgo()
        try:
            if request.POST.get("accion") == "reparacion":
                services.marcar_en_reparacion(hallazgo, request.user)
                messages.success(request, "El hallazgo quedó en reparación.")
                return redirect("revisiones:hallazgo", pk=pk)
            form = FormularioCierreHallazgo(request.POST)
            if form.is_valid():
                services.cerrar_hallazgo(hallazgo, form.cleaned_data["acciones"], request.user)
                messages.success(request, "Hallazgo cerrado.")
                return redirect(request.POST.get("siguiente") or reverse("revisiones:hallazgo", args=[pk]))
        except ValidationError as error:
            form.add_error(None, error.messages[0])
        return render(request, self.template_name, {"hallazgo": hallazgo, "form": form})


# -------------------------------------------------------- Notificaciones ----

class NotificacionListaView(ListView):
    """CU-A3 Consultar notificaciones."""

    template_name = "revisiones/notificacion_lista.html"
    context_object_name = "notificaciones"
    paginate_by = 30

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user).select_related(
            "revision__asignacion__material")


class NotificacionAbrirView(View):
    """Abrir un aviso lo marca como leído con su fecha (RF-09)."""

    def get(self, request, pk):
        aviso = get_object_or_404(Notificacion.objects.select_related("revision"), pk=pk, usuario=request.user)
        aviso.marcar_leida()
        revision = aviso.revision
        if revision is None:
            return redirect("revisiones:notificaciones")
        if revision.ejecutable and services.puede_ejecutar(revision, request.user) \
                and revision.usuario_responsable_id == request.user.pk:
            return redirect("revisiones:ejecutar", pk=revision.pk)
        if aviso.tipo == "hallazgo" and request.user.tiene_permiso("hallazgo.gestionar"):
            hallazgo = revision.hallazgos.first()
            if hallazgo:
                return redirect("revisiones:hallazgo", pk=hallazgo.pk)
        return redirect("revisiones:detalle", pk=revision.pk)


class MarcarTodasLeidasView(View):
    def post(self, request):
        total = Notificacion.objects.filter(usuario=request.user, leida=False).update(
            leida=True, fecha_lectura=timezone.now())
        messages.success(request, f"{total} avisos marcados como leídos.")
        return redirect("revisiones:notificaciones")

