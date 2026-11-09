import tempfile
from datetime import datetime, time
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Replace, Upper
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView, UpdateView

from nucleo import respaldos
from nucleo.almacenamiento import ErrorAlmacenamiento, foto_de_perfil
from nucleo.enums import AccionAuditoria
from nucleo.utilidades import ip_cliente, limpiar_rut

from . import auditoria, demo
from .forms import (FiltroBitacora, FiltroUsuarios, FormularioCambioContrasena, FormularioFotoPerfil,
                    FormularioIngreso, FormularioPerfil, FormularioRestablecerContrasena,
                    FormularioRestaurarRespaldo, FormularioUsuario)
from .models import EventoAuditoria, FotoPerfil, Permiso, Rol, RolPermiso, Usuario
from .permisos import PermisoRequeridoMixin

# Permisos que el rol administrador conserva siempre, para no perder el acceso.
PERMISOS_PROTEGIDOS_ADMIN = {"usuario.administrar", "permiso.administrar", "respaldo.administrar"}


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

    def get_context_data(self, **kwargs):
        return super().get_context_data(form_foto=FormularioFotoPerfil(), **kwargs)


class PerfilEditarView(View):
    """El titular actualiza sus datos. El RUT y el rol los cambia el administrador."""

    template_name = "accesos/perfil_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": FormularioPerfil(instance=self._usuario(request))})

    def post(self, request):
        usuario = self._usuario(request)
        anteriores = auditoria.instantanea(usuario)
        form = FormularioPerfil(request.POST, instance=usuario)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        with transaction.atomic():
            form.save()
            antes, despues = auditoria.diferencias(anteriores, auditoria.instantanea(usuario))
            if despues:
                auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", usuario.pk, antes, despues)
        messages.success(request, "Datos actualizados.")
        return redirect("accesos:perfil")

    @staticmethod
    def _usuario(request):
        # Copia aparte: un formulario con errores no debe alterar al usuario de la sesión.
        return Usuario.objects.get(pk=request.user.pk)


class CambiarContrasenaView(auth_views.PasswordChangeView):
    """CU-A2 Cambiar contraseña propia."""

    template_name = "accesos/cambiar_contrasena.html"
    form_class = FormularioCambioContrasena
    success_url = reverse_lazy("accesos:perfil")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", self.request.user.pk,
                            nuevos={"contrasena": "cambiada por el titular"})
        messages.success(self.request, "Contraseña actualizada.")
        return respuesta


class FotoPerfilView(View):
    """La foto la ve el titular o quien administra usuarios."""

    def get(self, request, pk):
        if request.user.pk != pk and not request.user.tiene_permiso("usuario.administrar"):
            raise PermissionDenied
        foto = get_object_or_404(FotoPerfil, pk=pk)
        respuesta = HttpResponse(bytes(foto.imagen), content_type="image/jpeg")
        respuesta["Cache-Control"] = "private, max-age=86400"
        return respuesta


class FotoPerfilSubirView(View):
    """CU-A2: el titular sube o reemplaza su foto de perfil."""

    def post(self, request):
        form = FormularioFotoPerfil(request.POST, request.FILES)
        if not form.is_valid():
            for error in form.errors.get("foto", ["No se pudo procesar la imagen."]):
                messages.error(request, error)
            return redirect("accesos:perfil")
        try:
            imagen = foto_de_perfil(form.cleaned_data["foto"])
        except ErrorAlmacenamiento as error:
            messages.error(request, str(error))
            return redirect("accesos:perfil")
        with transaction.atomic():
            request.user.cambiar_foto(imagen)
            auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", request.user.pk,
                                nuevos={"foto_perfil": "actualizada por el titular"})
        messages.success(request, "Foto actualizada.")
        return redirect("accesos:perfil")


class FotoPerfilEliminarView(View):
    """El titular quita su foto y vuelve a las iniciales."""

    def post(self, request):
        if request.user.tiene_foto:
            with transaction.atomic():
                request.user.quitar_foto()
                auditoria.registrar(AccionAuditoria.MODIFICACION, "usuario", request.user.pk,
                                    nuevos={"foto_perfil": "eliminada por el titular"})
            messages.success(request, "Foto eliminada.")
        return redirect("accesos:perfil")


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
                condicion = (Q(nombre__icontains=q) | Q(apellidos__icontains=q) | Q(rut__icontains=q)
                             | Q(correo__icontains=q))
                # El RUT se guarda como 12.345.678-9: se compara sin puntos, guion ni mayúsculas,
                # para encontrarlo escrito de cualquier forma (123456789, 12345678-9, 12.345.678-9).
                rut_buscado = limpiar_rut(q)
                if any(c.isdigit() for c in rut_buscado):
                    usuarios = usuarios.annotate(rut_limpio=Upper(Replace(Replace(
                        "rut", Value("."), Value("")), Value("-"), Value(""))))
                    condicion |= Q(rut_limpio__contains=rut_buscado)
                usuarios = usuarios.filter(condicion)
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
        messages.success(self.request, "Usuario actualizado.")
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
        return redirect("accesos:usuarios")


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
            messages.success(request, "Permisos actualizados.")
        else:
            messages.info(request, "Sin cambios.")
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


# ------------------------------------------------------------- Respaldos ----

class RespaldosView(PermisoRequeridoMixin, View):
    """RNF-05: el administrador genera, descarga y restaura respaldos completos."""

    permiso_requerido = "respaldo.administrar"
    template_name = "accesos/respaldos.html"

    def get(self, request):
        return self.pantalla(request, FormularioRestaurarRespaldo(usuario=request.user))

    @classmethod
    def pantalla(cls, request, form, status=200):
        return render(request, cls.template_name, {"respaldos": respaldos.listar(), "form": form}, status=status)


class RespaldoCrearView(PermisoRequeridoMixin, View):
    permiso_requerido = "respaldo.administrar"

    def post(self, request):
        try:
            ruta = respaldos.crear_respaldo("manuales")
        except respaldos.ErrorRespaldo as exc:
            messages.error(request, f"No se pudo generar el respaldo. {exc}")
            return redirect("accesos:respaldos")
        auditoria.registrar(AccionAuditoria.ALTA, "respaldo", ruta.name, nuevos={"bytes": ruta.stat().st_size})
        messages.success(request, f"Respaldo {ruta.name} generado. Descárguelo y guárdelo fuera del servidor.")
        return redirect("accesos:respaldos")


class RespaldoDescargarView(PermisoRequeridoMixin, View):
    permiso_requerido = "respaldo.administrar"

    def get(self, request, carpeta, nombre):
        try:
            ruta = respaldos.obtener(carpeta, nombre)
        except respaldos.ErrorRespaldo:
            raise Http404("Respaldo no encontrado.")
        auditoria.registrar(AccionAuditoria.ACCESO, "respaldo", nombre, nuevos={"evento": "descarga"})
        return FileResponse(ruta.open("rb"), as_attachment=True, filename=nombre, content_type="application/zip")


class RespaldoEliminarView(PermisoRequeridoMixin, View):
    permiso_requerido = "respaldo.administrar"

    def post(self, request, carpeta, nombre):
        try:
            respaldos.eliminar(carpeta, nombre)
        except respaldos.ErrorRespaldo:
            raise Http404("Respaldo no encontrado.")
        auditoria.registrar(AccionAuditoria.BAJA, "respaldo", nombre, anteriores={"carpeta": carpeta})
        messages.success(request, f"Respaldo {nombre} eliminado.")
        return redirect("accesos:respaldos")


class RespaldoRestaurarView(PermisoRequeridoMixin, View):
    """Reemplaza todos los datos por los del respaldo. Antes guarda una copia del estado actual."""

    permiso_requerido = "respaldo.administrar"

    def post(self, request):
        form = FormularioRestaurarRespaldo(request.POST, request.FILES, usuario=request.user)
        if not form.is_valid():
            return RespaldosView.pantalla(request, form, status=400)
        correo, ip = request.user.correo, ip_cliente(request)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                ruta, nombre = self._archivo(form, Path(tmp))
                respaldos.leer_manifiesto(ruta)
                copia = respaldos.crear_respaldo("manuales", "antes_de_restaurar")
                manifiesto = respaldos.restaurar(ruta)
            except respaldos.ErrorRespaldo as exc:
                form.add_error(None, str(exc))
                return RespaldosView.pantalla(request, form, status=400)

        # La base restaurada trae sus propias sesiones: se cierran todas, también la actual.
        Session.objects.all().delete()
        usuario = Usuario.objects.filter(correo__iexact=correo).first() or auditoria.usuario_sistema()
        auditoria.registrar(AccionAuditoria.MODIFICACION, "respaldo", nombre, usuario=usuario, ip=ip,
                            anteriores={"copia_previa": copia.name},
                            nuevos={"evento": "restauracion", "creado": manifiesto["creado"],
                                    "version": manifiesto["version"]})
        request.session.flush()
        request.user = AnonymousUser()
        fecha = manifiesto["creado"][:16].replace("T", " ")
        messages.success(request, f"Datos restaurados desde el respaldo del {fecha}. Se guardó una copia del estado "
                                  f"anterior ({copia.name}). Ingrese nuevamente.")
        return redirect("accesos:login")

    @staticmethod
    def _archivo(form, tmp):
        subido = form.cleaned_data.get("archivo")
        if subido:
            destino = tmp / "subido.zip"
            with destino.open("wb") as salida:
                for trozo in subido.chunks():
                    salida.write(trozo)
            return destino, Path(subido.name).name[:40]
        carpeta, _, nombre = form.cleaned_data["origen"].partition("/")
        return respaldos.obtener(carpeta, nombre), nombre
