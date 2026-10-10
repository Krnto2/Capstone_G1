from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView, UpdateView

from nucleo.enums import AccionAuditoria

from . import auditoria, demo
from .forms import (FiltroBitacora, FiltroUsuarios, FormularioCambioContrasena, FormularioIngreso,
                    FormularioRestablecerContrasena, FormularioUsuario)
from .models import EventoAuditoria, Permiso, Rol, RolPermiso, Usuario
from .permisos import PermisoRequeridoMixin

# Permisos que el rol administrador conserva siempre, para no perder el acceso.
PERMISOS_PROTEGIDOS_ADMIN = {"usuario.administrar", "permiso.administrar"}


class IngresarView(auth_views.LoginView):
    """CU-A1 Iniciar sesión (pantalla M1)."""

    template_name = "registration/login.html"
    authentication_form = FormularioIngreso
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        usuarios = demo.usuarios_visibles()
        return super().get_context_data(usuarios_demo=usuarios,
                                        contrasena_demo=demo.CONTRASENA_DEMO if usuarios else None, **kwargs)


class SalirView(auth_views.LogoutView):
    pass


class PerfilView(TemplateView):
    template_name = "accesos/perfil.html"


class CambiarContrasenaView(auth_views.PasswordChangeView):
    """CU-A2 Cambiar contraseña propia."""

    template_name = "accesos/cambiar_contrasena.html"
    form_class = FormularioCambioContrasena
    success_url = reverse_lazy("accesos:perfil")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", self.request.user.pk,
                            nuevos={"contrasena": "cambiada por el titular"})
        messages.success(self.request, "Su contraseña fue actualizada.")
        return respuesta


# ------------------------------------------------------------- Usuarios ----

class UsuarioListaView(PermisoRequeridoMixin, ListView):
    """CU-A4 Administrar usuarios."""

    permiso_requerido = "usuario.administrar"
    template_name = "accesos/usuario_lista.html"
    context_object_name = "usuarios"
    paginate_by = 25

    def get_queryset(self):
        self.filtro = FiltroUsuarios(self.request.GET or None)
        usuarios = Usuario.objects.personas().select_related("rol")
        if self.filtro.is_valid():
            datos = self.filtro.cleaned_data
            if datos["q"]:
                q = datos["q"].strip()
                usuarios = usuarios.filter(Q(nombre__icontains=q) | Q(apellidos__icontains=q)
                                           | Q(rut__icontains=q) | Q(correo__icontains=q))
            if datos["rol"]:
                usuarios = usuarios.filter(rol=datos["rol"])
            if datos["estado"]:
                usuarios = usuarios.filter(activo=datos["estado"] == "activo")
        return usuarios

    def get_context_data(self, **kwargs):
        return super().get_context_data(filtro=self.filtro, **kwargs)


class UsuarioCrearView(PermisoRequeridoMixin, CreateView):
    permiso_requerido = "usuario.administrar"
    model = Usuario
    form_class = FormularioUsuario
    template_name = "accesos/usuario_form.html"
    success_url = reverse_lazy("accesos:usuarios")

    @transaction.atomic
    def form_valid(self, form):
        respuesta = super().form_valid(form)
        auditoria.registrar(AccionAuditoria.ALTA, "usuario", self.object.pk,
                            nuevos=auditoria.instantanea(self.object))
        messages.success(self.request, f"Usuario {self.object.nombre_completo} creado.")
        return respuesta


class UsuarioEditarView(PermisoRequeridoMixin, UpdateView):
    """CU-A4 y CU-A5 Asignar rol a usuario."""

    permiso_requerido = "usuario.administrar"
    model = Usuario
    form_class = FormularioUsuario
    template_name = "accesos/usuario_form.html"
    success_url = reverse_lazy("accesos:usuarios")

    def get_queryset(self):
        return Usuario.objects.personas()

    @transaction.atomic
    def form_valid(self, form):
        anteriores = auditoria.instantanea(Usuario.objects.get(pk=self.object.pk))
        respuesta = super().form_valid(form)
        antes, despues = auditoria.diferencias(anteriores, auditoria.instantanea(self.object))
        if despues:
            auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", self.object.pk, antes, despues)
        messages.success(self.request, "Los datos del usuario fueron actualizados.")
        return respuesta


class UsuarioEstadoView(PermisoRequeridoMixin, View):
    """Desactivar o reactivar una cuenta (RF-01)."""

    permiso_requerido = "usuario.administrar"

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario.objects.personas(), pk=pk)
        try:
            with transaction.atomic():
                if usuario.activo:
                    usuario.desactivar()
                    accion, texto = AccionAuditoria.BAJA, "desactivada"
                else:
                    usuario.activo = True
                    usuario.save(update_fields=["activo"])
                    accion, texto = AccionAuditoria.ALTA, "reactivada"
                auditoria.registrar(accion, "usuario", usuario.pk, {"activo": not usuario.activo},
                                    {"activo": usuario.activo})
            messages.success(request, f"La cuenta de {usuario.nombre_completo} fue {texto}.")
        except ValidationError as error:
            messages.error(request, error.messages[0])
        return redirect(request.POST.get("siguiente") or "accesos:usuarios")


class UsuarioContrasenaView(PermisoRequeridoMixin, FormView):
    """El administrador restablece la contraseña de un usuario."""

    permiso_requerido = "usuario.administrar"
    template_name = "accesos/usuario_contrasena.html"
    form_class = FormularioRestablecerContrasena

    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(Usuario.objects.personas(), pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.usuario
        return kwargs

    def form_valid(self, form):
        form.save()
        auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", self.usuario.pk,
                            nuevos={"contrasena": "restablecida por el administrador"})
        messages.success(self.request, f"Contraseña de {self.usuario.nombre_completo} restablecida.")
        return redirect("accesos:usuarios")

    def get_context_data(self, **kwargs):
        return super().get_context_data(usuario_objetivo=self.usuario, **kwargs)


# ------------------------------------------------------------- Permisos ----

class PermisosRolView(PermisoRequeridoMixin, View):
    """CU-A6 Administrar permisos por rol."""

    permiso_requerido = "permiso.administrar"
    template_name = "accesos/permisos_rol.html"

    def _matriz(self):
        roles = list(Rol.objects.all())
        asignados = set(RolPermiso.objects.values_list("rol_id", "permiso_id"))
        modulos = {}
        for permiso in Permiso.objects.all():
            fila = {"permiso": permiso,
                    "celdas": [{"rol": rol, "marcado": (rol.pk, permiso.pk) in asignados,
                                "protegido": rol.nombre == Rol.ADMINISTRADOR
                                and permiso.codigo in PERMISOS_PROTEGIDOS_ADMIN}
                               for rol in roles]}
            modulos.setdefault(permiso.modulo, []).append(fila)
        return roles, modulos

    def get(self, request):
        roles, modulos = self._matriz()
        return render(request, self.template_name, {"roles": roles, "modulos": modulos})

    @transaction.atomic
    def post(self, request):
        roles = list(Rol.objects.all())
        permisos = {p.pk: p for p in Permiso.objects.all()}
        cambios = 0
        for rol in roles:
            actuales = set(RolPermiso.objects.filter(rol=rol).values_list("permiso_id", flat=True))
            nuevos = {int(v) for v in request.POST.getlist(f"rol_{rol.pk}") if v.isdigit() and int(v) in permisos}
            if rol.nombre == Rol.ADMINISTRADOR:
                nuevos |= {pk for pk, p in permisos.items() if p.codigo in PERMISOS_PROTEGIDOS_ADMIN}
            if nuevos == actuales:
                continue
            RolPermiso.objects.filter(rol=rol, permiso_id__in=actuales - nuevos).delete()
            RolPermiso.objects.bulk_create([RolPermiso(rol=rol, permiso_id=pk) for pk in nuevos - actuales])
            auditoria.registrar(
                AccionAuditoria.MODIFICACION, "rol_permiso", rol.pk,
                {"permisos": sorted(permisos[pk].codigo for pk in actuales)},
                {"permisos": sorted(permisos[pk].codigo for pk in nuevos)},
            )
            cambios += 1
        if cambios:
            messages.success(request, "Los permisos fueron actualizados.")
        else:
            messages.info(request, "No hubo cambios en los permisos.")
        return redirect("accesos:permisos")


# ------------------------------------------------------------- Bitácora ----

class BitacoraView(PermisoRequeridoMixin, ListView):
    """CU-A7 Consultar bitácora de auditoría (solo lectura)."""

    permiso_requerido = "auditoria.consultar"
    template_name = "accesos/bitacora.html"
    context_object_name = "eventos"
    paginate_by = 50

    def get_queryset(self):
        self.filtro = FiltroBitacora(self.request.GET or None)
        eventos = EventoAuditoria.objects.select_related("usuario")
        if self.filtro.is_valid():
            datos = self.filtro.cleaned_data
            if datos["usuario"]:
                eventos = eventos.filter(usuario=datos["usuario"])
            if datos["accion"]:
                eventos = eventos.filter(accion=datos["accion"])
            if datos["entidad"]:
                eventos = eventos.filter(entidad_afectada__icontains=datos["entidad"].strip())
            zona = timezone.get_current_timezone()
            if datos["desde"]:
                eventos = eventos.filter(fecha_hora__gte=datetime.combine(datos["desde"], time.min, zona))
            if datos["hasta"]:
                eventos = eventos.filter(fecha_hora__lte=datetime.combine(datos["hasta"], time.max, zona))
        return eventos

    def get_context_data(self, **kwargs):
        return super().get_context_data(filtro=self.filtro, **kwargs)
