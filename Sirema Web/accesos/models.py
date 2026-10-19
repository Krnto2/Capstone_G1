"""
Módulo de accesos: rol, permiso, rol_permiso, usuario y evento_auditoria.

Los nombres de tablas y columnas son los del modelo relacional de la Fase 2.
"""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from nucleo.enums import AccionAuditoria, restriccion_enum

CORREO_SISTEMA = "sistema@sirema.local"


class Rol(models.Model):
    ADMINISTRADOR = "administrador"
    JEFATURA = "jefatura"
    BOMBERO = "bombero"

    id = models.AutoField(primary_key=True, db_column="id_rol")
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "rol"
        ordering = ["id"]
        verbose_name = "rol"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.nombre.capitalize()

    def permisos(self):
        return Permiso.objects.filter(asignaciones_rol__rol=self).order_by("modulo", "codigo")


class Permiso(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_permiso")
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=80)
    modulo = models.CharField(max_length=30)

    class Meta:
        db_table = "permiso"
        ordering = ["modulo", "codigo"]

    def __str__(self):
        return self.nombre


class RolPermiso(models.Model):
    """Tabla intermedia rol-permiso con clave primaria compuesta."""

    pk = models.CompositePrimaryKey("rol_id", "permiso_id")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column="id_rol",
                            related_name="asignaciones_permiso")
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, db_column="id_permiso",
                                related_name="asignaciones_rol")

    class Meta:
        db_table = "rol_permiso"


class UsuarioQuerySet(models.QuerySet):
    def personas(self):
        """Excluye al usuario técnico «sistema»."""
        return self.exclude(correo=CORREO_SISTEMA)

    def activos(self):
        return self.personas().filter(activo=True)

    def con_permiso(self, codigo):
        return self.activos().filter(rol__asignaciones_permiso__permiso__codigo=codigo,
                                     rol__activo=True).distinct()


class UsuarioManager(BaseUserManager.from_queryset(UsuarioQuerySet)):
    use_in_migrations = True

    def create_user(self, correo, password=None, **campos):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        usuario = self.model(correo=self.normalize_email(correo).lower(), **campos)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def get_by_natural_key(self, correo):
        return self.get(correo__iexact=correo)


class Usuario(AbstractBaseUser):
    """Bombero de la compañía con credenciales y exactamente un rol."""

    id = models.AutoField(primary_key=True, db_column="id_usuario")
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column="id_rol", related_name="usuarios")
    rut = models.CharField("RUT", max_length=12, unique=True)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    correo = models.EmailField(max_length=120, unique=True)
    password = models.CharField("contraseña", max_length=255, db_column="hash_contrasena")
    telefono = models.CharField("teléfono", max_length=15, null=True, blank=True)
    foto_perfil = models.CharField("foto de perfil", max_length=300, null=True, blank=True,
                                   db_column="foto_perfil")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField("último acceso", null=True, blank=True, db_column="ultimo_acceso")

    objects = UsuarioManager()

    USERNAME_FIELD = "correo"
    EMAIL_FIELD = "correo"
    REQUIRED_FIELDS = ["rut", "nombre", "apellidos"]

    class Meta:
        db_table = "usuario"
        ordering = ["apellidos", "nombre"]

    def __str__(self):
        return self.nombre_completo

    @property
    def is_active(self):
        return self.activo

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}".strip()

    @property
    def nombre_corto(self):
        """J. Soto"""
        primer_apellido = self.apellidos.split(" ")[0] if self.apellidos else ""
        return f"{self.nombre[:1]}. {primer_apellido}".strip()

    @property
    def iniciales(self):
        return f"{self.nombre[:1]}{self.apellidos[:1]}".upper()

    @property
    def tiene_foto(self):
        return bool(self.foto_perfil)

    @property
    def foto_version(self):
        """Token breve para refrescar la caché del navegador al cambiar la foto."""
        return (self.foto_perfil or "")[-20:]

    @property
    def es_sistema(self):
        return self.correo == CORREO_SISTEMA

    def permisos_codigos(self):
        if not hasattr(self, "_permisos_cache"):
            if not self.activo or not self.rol.activo:
                self._permisos_cache = frozenset()
            else:
                self._permisos_cache = frozenset(
                    Permiso.objects.filter(asignaciones_rol__rol_id=self.rol_id).values_list("codigo", flat=True)
                )
        return self._permisos_cache

    def tiene_permiso(self, codigo):
        return codigo in self.permisos_codigos()

    def clean(self):
        super().clean()
        self.correo = (self.correo or "").strip().lower()

    def es_unico_administrador_activo(self):
        if not (self.pk and self.activo and self.rol.nombre == Rol.ADMINISTRADOR):
            return False
        return not Usuario.objects.activos().filter(rol__nombre=Rol.ADMINISTRADOR).exclude(pk=self.pk).exists()

    def desactivar(self):
        """RF-01: un usuario desactivado no ingresa, pero conserva su historial."""
        if self.es_unico_administrador_activo():
            raise ValidationError("No se puede desactivar al único administrador activo.")
        self.activo = False
        self.save(update_fields=["activo"])


class EventoAuditoria(models.Model):
    """Bitácora inmutable (RNF-09). Un disparador rechaza UPDATE y DELETE."""

    id = models.BigAutoField(primary_key=True, db_column="id_evento")
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, db_column="id_usuario",
                                related_name="eventos_auditoria")
    fecha_hora = models.DateTimeField(default=timezone.now, db_index=True)
    accion = models.CharField(max_length=20, choices=AccionAuditoria.choices)
    entidad_afectada = models.CharField(max_length=40)
    id_registro = models.CharField(max_length=40)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "evento_auditoria"
        ordering = ["-fecha_hora", "-id"]
        constraints = [restriccion_enum("accion", AccionAuditoria, "ck_evento_accion")]
        indexes = [models.Index(fields=["entidad_afectada", "id_registro"], name="ix_evento_entidad")]

    def __str__(self):
        return f"{self.fecha_hora:%d-%m-%Y %H:%M} {self.get_accion_display()} {self.entidad_afectada}"

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("La bitácora de auditoría no se puede modificar.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("La bitácora de auditoría no se puede eliminar.")
