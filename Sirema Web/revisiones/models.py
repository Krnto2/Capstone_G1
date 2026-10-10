"""
Módulo de revisiones: plan_revision, punto_control, asignacion_plan, revision,
resultado_punto, fotografia, hallazgo y notificacion.

Cadena principal: material -> asignacion_plan -> revision -> resultado_punto ->
fotografia. El único enlace con el inventario es asignacion_plan.id_material.
"""
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from nucleo.enums import (CriticidadHallazgo, EstadoHallazgo, EstadoRevision, ResultadoControl, TipoDatoPunto,
                          TipoNotificacion, UnidadFrecuencia, restriccion_enum)
from nucleo.utilidades import a_decimal, hoy, sumar_periodo


class PlanRevision(models.Model):
    """Plantilla de control: qué se revisa y con qué frecuencia."""

    id = models.AutoField(primary_key=True, db_column="id_plan")
    nombre = models.CharField(max_length=100)
    version = models.SmallIntegerField("versión", default=1)
    descripcion = models.CharField("descripción e indicaciones del fabricante", max_length=300, null=True,
                                   blank=True)
    frecuencia_valor = models.SmallIntegerField("cada", default=1)
    frecuencia_unidad = models.CharField("unidad", max_length=10, choices=UnidadFrecuencia.choices,
                                         default=UnidadFrecuencia.SEMANA)
    dias_tolerancia = models.SmallIntegerField("días de tolerancia", default=0)
    exige_fotografia = models.BooleanField("exige fotografía general", default=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "plan_revision"
        ordering = ["nombre", "-version"]
        verbose_name = "plan de revisión"
        verbose_name_plural = "planes de revisión"
        constraints = [
            models.UniqueConstraint(fields=["nombre", "version"], name="uq_plan_nombre_version"),
            models.CheckConstraint(condition=Q(frecuencia_valor__gte=1), name="ck_plan_frecuencia"),
            models.CheckConstraint(condition=Q(dias_tolerancia__gte=0), name="ck_plan_tolerancia"),
            restriccion_enum("frecuencia_unidad", UnidadFrecuencia, "ck_plan_frecuencia_unidad"),
        ]

    def __str__(self):
        return f"{self.nombre} v{self.version}"

    @property
    def frecuencia_legible(self):
        nombres = {"dia": ("diaria", "días"), "semana": ("semanal", "semanas"),
                   "mes": ("mensual", "meses"), "anio": ("anual", "años")}
        singular, plural = nombres[self.frecuencia_unidad]
        if self.frecuencia_valor == 1:
            return singular
        if self.frecuencia_unidad == "semana" and self.frecuencia_valor == 2:
            return "quincenal"
        return f"cada {self.frecuencia_valor} {plural}"

    def proxima_fecha(self, desde):
        return sumar_periodo(desde, self.frecuencia_valor, self.frecuencia_unidad)

    def fecha_programada(self, inicio, n):
        """n-ésima fecha del calendario contada desde el inicio (sin acumular desfases)."""
        return sumar_periodo(inicio, self.frecuencia_valor, self.frecuencia_unidad, veces=n)

    def tiene_historial(self):
        return Revision.objects.filter(asignacion__plan=self).exists()


class PuntoControl(models.Model):
    """Ítem que se verifica o se mide en una revisión."""

    id = models.AutoField(primary_key=True, db_column="id_punto")
    plan = models.ForeignKey(PlanRevision, on_delete=models.CASCADE, db_column="id_plan", related_name="puntos")
    numero_orden = models.SmallIntegerField("orden")
    descripcion = models.CharField("acción a verificar", max_length=200)
    tipo_dato = models.CharField("tipo de dato", max_length=10, choices=TipoDatoPunto.choices,
                                 default=TipoDatoPunto.BOOLEANO)
    unidad_medida = models.CharField("unidad de medida", max_length=15, null=True, blank=True)
    valor_minimo = models.DecimalField("mínimo", max_digits=10, decimal_places=2, null=True, blank=True)
    valor_maximo = models.DecimalField("máximo", max_digits=10, decimal_places=2, null=True, blank=True)
    obligatorio = models.BooleanField(default=True)
    exige_fotografia = models.BooleanField("exige foto", default=False)

    class Meta:
        db_table = "punto_control"
        ordering = ["plan", "numero_orden"]
        constraints = [
            models.UniqueConstraint(fields=["plan", "numero_orden"], name="uq_punto_plan_orden"),
            models.CheckConstraint(condition=Q(valor_minimo__isnull=True) | Q(valor_maximo__isnull=True)
                                   | Q(valor_maximo__gte=F("valor_minimo")), name="ck_punto_rango"),
            restriccion_enum("tipo_dato", TipoDatoPunto, "ck_punto_tipo_dato"),
        ]

    def __str__(self):
        return f"{self.numero_orden}. {self.descripcion}"

    @property
    def tiene_rango(self):
        return self.valor_minimo is not None or self.valor_maximo is not None

    @property
    def rango_legible(self):
        def fmt(v):
            return f"{v.normalize():f}".replace(".", ",")

        if self.valor_minimo is not None and self.valor_maximo is not None:
            return f"{fmt(self.valor_minimo)} a {fmt(self.valor_maximo)}"
        if self.valor_minimo is not None:
            return f"mínimo {fmt(self.valor_minimo)}"
        if self.valor_maximo is not None:
            return f"máximo {fmt(self.valor_maximo)}"
        return ""

    def fuera_de_rango(self, valor):
        numero = a_decimal(valor)
        if numero is None or self.tipo_dato != TipoDatoPunto.NUMERICO:
            return False
        return ((self.valor_minimo is not None and numero < self.valor_minimo)
                or (self.valor_maximo is not None and numero > self.valor_maximo))

    def evaluar(self, valor):
        """Resultado sugerido para un valor: falla si queda fuera del rango aceptable."""
        if self.tipo_dato == TipoDatoPunto.NUMERICO and self.fuera_de_rango(valor):
            return ResultadoControl.FALLA
        if self.tipo_dato == TipoDatoPunto.BOOLEANO and str(valor).lower() in ("no", "false", "0"):
            return ResultadoControl.FALLA
        return ResultadoControl.CONFORME


class AsignacionPlan(models.Model):
    """Vínculo vigente entre un plan, un elemento del inventario y su responsable."""

    id = models.AutoField(primary_key=True, db_column="id_asignacion")
    plan = models.ForeignKey(PlanRevision, on_delete=models.RESTRICT, db_column="id_plan",
                             related_name="asignaciones")
    # Enlace entre módulos: el elemento del inventario que será revisado.
    material = models.ForeignKey("inventario.Material", on_delete=models.RESTRICT, db_column="id_material",
                                 related_name="asignaciones")
    usuario_responsable = models.ForeignKey("accesos.Usuario", on_delete=models.SET_NULL, null=True, blank=True,
                                            db_column="id_usuario_responsable",
                                            related_name="asignaciones_responsable", verbose_name="responsable")
    fecha_inicio = models.DateField("fecha de inicio")
    fecha_termino = models.DateField("fecha de término", null=True, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "asignacion_plan"
        ordering = ["-activa", "material__codigo_institucional"]
        constraints = [
            models.UniqueConstraint(fields=["material", "plan"], condition=Q(activa=True),
                                    name="uq_asignacion_activa_material_plan"),
            models.CheckConstraint(condition=Q(fecha_termino__isnull=True) | Q(fecha_termino__gte=F("fecha_inicio")),
                                   name="ck_asignacion_fechas"),
        ]

    def __str__(self):
        return f"{self.plan} → {self.material}"

    def cerrar(self, fecha=None):
        self.activa = False
        fecha = fecha or hoy()
        self.fecha_termino = max(fecha, self.fecha_inicio)
        self.save(update_fields=["activa", "fecha_termino"])


class RevisionQuerySet(models.QuerySet):
    ABIERTAS = (EstadoRevision.PENDIENTE, EstadoRevision.EN_CURSO, EstadoRevision.VENCIDA)

    def completa(self):
        return self.select_related("asignacion__plan", "asignacion__material__cajonera__unidad",
                                   "asignacion__material__categoria", "usuario_responsable", "usuario_ejecutor")

    def abiertas(self):
        return self.filter(estado__in=self.ABIERTAS)

    def pendientes_de(self, usuario):
        return self.filter(usuario_responsable=usuario, estado__in=self.ABIERTAS)

    def por_urgencia(self):
        return self.order_by("fecha_limite", "fecha_programada", "id")


class Revision(models.Model):
    """Aplicación de un plan a un elemento en una fecha."""

    id = models.AutoField(primary_key=True, db_column="id_revision")
    asignacion = models.ForeignKey(AsignacionPlan, on_delete=models.RESTRICT, db_column="id_asignacion",
                                   related_name="revisiones")
    usuario_responsable = models.ForeignKey("accesos.Usuario", on_delete=models.RESTRICT,
                                            db_column="id_usuario_responsable",
                                            related_name="revisiones_responsable", verbose_name="responsable")
    usuario_ejecutor = models.ForeignKey("accesos.Usuario", on_delete=models.RESTRICT, null=True, blank=True,
                                         db_column="id_usuario_ejecutor", related_name="revisiones_ejecutadas")
    fecha_programada = models.DateField()
    fecha_limite = models.DateField("fecha límite")
    estado = models.CharField(max_length=15, choices=EstadoRevision.choices, default=EstadoRevision.PENDIENTE)
    fecha_hora_inicio = models.DateTimeField(null=True, blank=True)
    fecha_hora_termino = models.DateTimeField(null=True, blank=True)
    resultado_global = models.CharField(max_length=15, choices=ResultadoControl.choices, null=True, blank=True)
    observaciones = models.CharField(max_length=500, null=True, blank=True)

    objects = RevisionQuerySet.as_manager()

    class Meta:
        db_table = "revision"
        ordering = ["-fecha_programada", "-id"]
        verbose_name = "revisión"
        verbose_name_plural = "revisiones"
        constraints = [
            # DAS 4.2.5: el programador de tareas no duplica revisiones.
            models.UniqueConstraint(fields=["asignacion", "fecha_programada"], name="uq_revision_asignacion_fecha"),
            models.CheckConstraint(condition=Q(fecha_hora_termino__isnull=True) | Q(fecha_hora_inicio__isnull=True)
                                   | Q(fecha_hora_termino__gte=F("fecha_hora_inicio")), name="ck_revision_horas"),
            models.CheckConstraint(condition=Q(fecha_limite__gte=F("fecha_programada")), name="ck_revision_limite"),
            restriccion_enum("estado", EstadoRevision, "ck_revision_estado"),
            restriccion_enum("resultado_global", ResultadoControl, "ck_revision_resultado", nulo=True),
        ]
        indexes = [models.Index(fields=["estado", "fecha_limite"], name="ix_revision_estado_limite"),
                   models.Index(fields=["usuario_responsable", "estado"], name="ix_revision_responsable")]

    def __str__(self):
        return f"Revisión {self.material} · {self.fecha_programada:%d-%m-%Y}"

    @property
    def material(self):
        return self.asignacion.material

    @property
    def plan(self):
        return self.asignacion.plan

    @property
    def ejecutable(self):
        return self.estado in RevisionQuerySet.ABIERTAS

    @property
    def en_plazo(self):
        if self.estado != EstadoRevision.REALIZADA or not self.fecha_hora_termino:
            return None
        return timezone.localdate(self.fecha_hora_termino) <= self.fecha_limite

    @property
    def dias_para_limite(self):
        return (self.fecha_limite - hoy()).days

    @property
    def urgencia(self):
        """vencida, hoy, pronto o normal: define el color de la tarjeta (M2)."""
        if self.estado == EstadoRevision.VENCIDA or (self.ejecutable and self.dias_para_limite < 0):
            return "vencida"
        if self.ejecutable and self.dias_para_limite == 0:
            return "hoy"
        if self.ejecutable and self.dias_para_limite == 1:
            return "pronto"
        return "normal"

    def calcular_resultado_global(self, resultados=None):
        """RF-08: falla si hay alguna falla, observación si hay alguna, conforme en otro caso."""
        valores = {r.resultado for r in (resultados if resultados is not None else self.resultados.all())}
        if ResultadoControl.FALLA in valores:
            return ResultadoControl.FALLA
        if ResultadoControl.OBSERVACION in valores:
            return ResultadoControl.OBSERVACION
        return ResultadoControl.CONFORME


class ResultadoPunto(models.Model):
    """Respuesta a un punto de control dentro de una revisión (clave compuesta)."""

    pk = models.CompositePrimaryKey("revision_id", "punto_id")
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE, db_column="id_revision",
                                 related_name="resultados")
    punto = models.ForeignKey(PuntoControl, on_delete=models.RESTRICT, db_column="id_punto",
                              related_name="resultados")
    valor_registrado = models.CharField(max_length=100, null=True, blank=True)
    resultado = models.CharField(max_length=15, choices=ResultadoControl.choices)
    observacion = models.CharField("observación", max_length=300, null=True, blank=True)
    fecha_hora_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "resultado_punto"
        ordering = ["punto__numero_orden"]
        constraints = [
            restriccion_enum("resultado", ResultadoControl, "ck_resultado_valor"),
            # RF-08: observación o falla exigen comentario.
            models.CheckConstraint(condition=Q(resultado=ResultadoControl.CONFORME)
                                   | (Q(observacion__isnull=False) & ~Q(observacion="")),
                                   name="ck_resultado_observacion"),
        ]

    def __str__(self):
        return f"{self.punto} · {self.get_resultado_display()}"


class Fotografia(models.Model):
    """Evidencia gráfica. La imagen vive en el volumen media, no en la base."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id_fotografia")
    revision = models.ForeignKey(Revision, on_delete=models.RESTRICT, db_column="id_revision",
                                 related_name="fotografias")
    # Con id_revision forma la clave foránea compuesta hacia resultado_punto, que la
    # migración 0002 crea con SQL explícito en PostgreSQL (DAS 4.2.5).
    punto = models.ForeignKey(PuntoControl, on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                              blank=True, db_column="id_punto", related_name="fotografias")
    usuario = models.ForeignKey("accesos.Usuario", on_delete=models.RESTRICT, db_column="id_usuario",
                                related_name="fotografias")
    nombre_archivo = models.CharField(max_length=150)
    ruta_almacenamiento = models.CharField(max_length=300)
    tipo_mime = models.CharField(max_length=30)
    tamano_bytes = models.BigIntegerField()
    hash_sha256 = models.CharField(max_length=64, unique=True)
    fecha_hora_captura = models.DateTimeField()
    fecha_hora_carga = models.DateTimeField(default=timezone.now)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    anulada = models.BooleanField(default=False)

    class Meta:
        db_table = "fotografia"
        ordering = ["fecha_hora_carga"]
        verbose_name = "fotografía"
        constraints = [
            models.CheckConstraint(condition=Q(tipo_mime__in=["image/jpeg", "image/png", "image/webp"]),
                                   name="ck_foto_tipo_mime"),
            models.CheckConstraint(condition=Q(tamano_bytes__gt=0), name="ck_foto_tamano"),
            models.CheckConstraint(condition=Q(fecha_hora_captura__lte=F("fecha_hora_carga")),
                                   name="ck_foto_fechas"),
        ]

    def __str__(self):
        return f"Fotografía {self.id}"


class Hallazgo(models.Model):
    """Falla detectada en una revisión, abierta hasta que la jefatura la cierra."""

    id = models.AutoField(primary_key=True, db_column="id_hallazgo")
    revision = models.ForeignKey(Revision, on_delete=models.RESTRICT, db_column="id_revision",
                                 related_name="hallazgos")
    usuario_cierre = models.ForeignKey("accesos.Usuario", on_delete=models.SET_NULL, null=True, blank=True,
                                       db_column="id_usuario_cierre", related_name="hallazgos_cerrados")
    descripcion = models.CharField("descripción", max_length=500)
    criticidad = models.CharField(max_length=10, choices=CriticidadHallazgo.choices)
    estado = models.CharField(max_length=15, choices=EstadoHallazgo.choices, default=EstadoHallazgo.ABIERTO)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    acciones = models.CharField("acciones tomadas", max_length=500, null=True, blank=True)

    class Meta:
        db_table = "hallazgo"
        ordering = ["-fecha_apertura"]
        constraints = [
            restriccion_enum("criticidad", CriticidadHallazgo, "ck_hallazgo_criticidad"),
            restriccion_enum("estado", EstadoHallazgo, "ck_hallazgo_estado"),
            models.CheckConstraint(condition=Q(fecha_cierre__isnull=True) | Q(fecha_cierre__gte=F("fecha_apertura")),
                                   name="ck_hallazgo_fechas"),
        ]

    def __str__(self):
        return f"Hallazgo {self.id} · {self.revision.material}"

    @property
    def abierto(self):
        return self.estado != EstadoHallazgo.CERRADO

    def cerrar(self, acciones, usuario):
        if not self.abierto:
            raise ValidationError("El hallazgo ya está cerrado.")
        if not (acciones or "").strip():
            raise ValidationError("Debe registrar la acción tomada.")
        self.estado = EstadoHallazgo.CERRADO
        self.acciones = acciones.strip()
        self.usuario_cierre = usuario
        self.fecha_cierre = timezone.now()
        self.save(update_fields=["estado", "acciones", "usuario_cierre", "fecha_cierre"])


class Notificacion(models.Model):
    """Aviso interno dirigido a un usuario (sin correo ni SMS)."""

    id = models.AutoField(primary_key=True, db_column="id_notificacion")
    usuario = models.ForeignKey("accesos.Usuario", on_delete=models.CASCADE, db_column="id_usuario",
                                related_name="notificaciones")
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE, null=True, blank=True, db_column="id_revision",
                                 related_name="notificaciones")
    tipo = models.CharField(max_length=15, choices=TipoNotificacion.choices)
    mensaje = models.CharField(max_length=300)
    fecha_generacion = models.DateTimeField(default=timezone.now)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    leida = models.BooleanField(default=False)

    class Meta:
        db_table = "notificacion"
        ordering = ["leida", "-fecha_generacion"]
        verbose_name = "notificación"
        verbose_name_plural = "notificaciones"
        constraints = [restriccion_enum("tipo", TipoNotificacion, "ck_notificacion_tipo")]
        indexes = [models.Index(fields=["usuario", "leida"], name="ix_notificacion_usuario")]

    def __str__(self):
        return self.mensaje

    def marcar_leida(self):
        """RF-09: una notificación abierta queda leída con su fecha."""
        if not self.leida:
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save(update_fields=["leida", "fecha_lectura"])
