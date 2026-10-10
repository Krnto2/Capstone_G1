"""
Módulo de inventario: unidad, cajonera, categoria, material, movimiento y baja.

Material es la tabla central del inventario. Las reglas que dependen solo de sus
datos viven en el modelo (trasladar, dar_de_baja); las que coordinan varios
pasos usan transacciones atómicas (RNF-08).
"""
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from accesos import auditoria
from nucleo.enums import AccionAuditoria, EstadoMaterial, TipoMaterial, TipoUnidad, restriccion_enum

from .signals import material_dado_de_baja


class Unidad(models.Model):
    """Carro de la compañía o bodega del cuartel."""

    id = models.AutoField(primary_key=True, db_column="id_unidad")
    codigo = models.CharField("código", max_length=10, unique=True)
    nombre = models.CharField(max_length=60)
    tipo = models.CharField(max_length=10, choices=TipoUnidad.choices, default=TipoUnidad.CARRO)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "unidad"
        ordering = ["codigo"]
        verbose_name_plural = "unidades"
        constraints = [restriccion_enum("tipo", TipoUnidad, "ck_unidad_tipo")]

    def __str__(self):
        return f"{self.codigo} · {self.nombre}"


class Cajonera(models.Model):
    """Compartimento de una unidad. No existe sin su unidad."""

    id = models.AutoField(primary_key=True, db_column="id_cajonera")
    unidad = models.ForeignKey(Unidad, on_delete=models.RESTRICT, db_column="id_unidad", related_name="cajoneras")
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField("descripción", max_length=150, null=True, blank=True)
    orden = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "cajonera"
        ordering = ["unidad__codigo", "orden", "nombre"]
        constraints = [models.UniqueConstraint(fields=["unidad", "nombre"], name="uq_cajonera_unidad_nombre")]

    def __str__(self):
        return f"{self.unidad.codigo} / {self.nombre}"


class Categoria(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_categoria")
    nombre = models.CharField(max_length=40, unique=True)
    descripcion = models.CharField("descripción", max_length=200, null=True, blank=True)

    class Meta:
        db_table = "categoria"
        ordering = ["nombre"]
        verbose_name = "categoría"

    def __str__(self):
        return self.nombre


class MaterialQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado=EstadoMaterial.ACTIVO)

    def con_ubicacion(self):
        return self.select_related("categoria", "cajonera", "cajonera__unidad")

    def buscar(self, texto):
        """RF-05: nombre o código parcial, desde el segundo carácter."""
        texto = (texto or "").strip()
        if len(texto) < 2:
            return self
        return self.filter(Q(nombre__icontains=texto) | Q(codigo_institucional__icontains=texto)
                           | Q(marca__icontains=texto) | Q(modelo__icontains=texto))


class Material(models.Model):
    """Ficha de un elemento de material menor."""

    id = models.AutoField(primary_key=True, db_column="id_material")
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, db_column="id_categoria",
                                  related_name="materiales", verbose_name="categoría")
    cajonera = models.ForeignKey(Cajonera, on_delete=models.RESTRICT, db_column="id_cajonera",
                                 related_name="materiales", verbose_name="ubicación")
    codigo_institucional = models.CharField("código institucional", max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TipoMaterial.choices, default=TipoMaterial.UNITARIO)
    cantidad = models.PositiveIntegerField(default=1)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero_serie = models.CharField("número de serie", max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=EstadoMaterial.choices, default=EstadoMaterial.ACTIVO)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    objects = MaterialQuerySet.as_manager()

    class Meta:
        db_table = "material"
        ordering = ["codigo_institucional", "nombre"]
        verbose_name_plural = "material"
        constraints = [
            # RF-04: índice único parcial, solo entre los elementos que registran código.
            models.UniqueConstraint(fields=["codigo_institucional"], condition=Q(codigo_institucional__isnull=False),
                                    name="uq_material_codigo_institucional"),
            models.CheckConstraint(condition=Q(cantidad__gte=1), name="ck_material_cantidad"),
            models.CheckConstraint(condition=Q(tipo=TipoMaterial.GRANEL) | Q(codigo_institucional__isnull=False),
                                   name="ck_material_unitario_con_codigo"),
            restriccion_enum("tipo", TipoMaterial, "ck_material_tipo"),
            restriccion_enum("estado", EstadoMaterial, "ck_material_estado"),
        ]
        indexes = [models.Index(fields=["estado", "nombre"], name="ix_material_estado_nombre")]

    def __str__(self):
        return f"{self.codigo_institucional} {self.nombre}" if self.codigo_institucional else self.nombre

    @property
    def activo(self):
        return self.estado == EstadoMaterial.ACTIVO

    @property
    def ubicacion(self):
        return str(self.cajonera)

    def trasladar(self, destino, usuario, motivo=None):
        """RF-06: registra el movimiento y actualiza la ubicación en una transacción."""
        if not self.activo:
            raise ValidationError("No se pueden mover elementos dados de baja.")
        if destino.pk == self.cajonera_id:
            raise ValidationError("El elemento ya se encuentra en esa ubicación.")
        with transaction.atomic():
            origen = self.cajonera
            movimiento = Movimiento.objects.create(material=self, cajonera_origen=origen, cajonera_destino=destino,
                                                   usuario=usuario, motivo=motivo or None)
            self.cajonera = destino
            self.save(update_fields=["cajonera", "fecha_actualizacion"])
            auditoria.registrar(AccionAuditoria.MOVIMIENTO, "material", self.pk,
                                {"id_cajonera": origen.pk, "ubicacion": str(origen)},
                                {"id_cajonera": destino.pk, "ubicacion": str(destino),
                                 "motivo": motivo or None, "id_movimiento": movimiento.pk},
                                usuario=usuario)
        return movimiento

    def dar_de_baja(self, motivo, usuario, destino_final=None):
        """RF-03: baja lógica. Conserva el historial y avisa a revisiones."""
        if not self.activo:
            raise ValidationError("El elemento ya está dado de baja.")
        if not (motivo or "").strip():
            raise ValidationError("Debe indicar el motivo de la baja.")
        with transaction.atomic():
            baja = Baja.objects.create(material=self, usuario=usuario, motivo=motivo.strip(),
                                       destino_final=destino_final or None)
            self.estado = EstadoMaterial.DE_BAJA
            self.save(update_fields=["estado", "fecha_actualizacion"])
            auditoria.registrar(AccionAuditoria.BAJA, "material", self.pk, {"estado": EstadoMaterial.ACTIVO},
                                {"estado": EstadoMaterial.DE_BAJA, "motivo": baja.motivo,
                                 "destino_final": baja.destino_final}, usuario=usuario)
            # Observador: revisiones cierra asignaciones y anula revisiones pendientes.
            material_dado_de_baja.send(sender=Material, material=self, usuario=usuario)
        return baja


class Movimiento(models.Model):
    """Traslado de un elemento entre cajoneras. El alta inicial no tiene origen."""

    id = models.AutoField(primary_key=True, db_column="id_movimiento")
    material = models.ForeignKey(Material, on_delete=models.RESTRICT, db_column="id_material",
                                 related_name="movimientos")
    cajonera_origen = models.ForeignKey(Cajonera, on_delete=models.RESTRICT, db_column="id_cajonera_origen",
                                        null=True, blank=True, related_name="movimientos_salida")
    cajonera_destino = models.ForeignKey(Cajonera, on_delete=models.RESTRICT, db_column="id_cajonera_destino",
                                         related_name="movimientos_entrada")
    usuario = models.ForeignKey("accesos.Usuario", on_delete=models.RESTRICT, db_column="id_usuario",
                                related_name="movimientos")
    fecha_hora = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "movimiento"
        ordering = ["-fecha_hora", "-id"]

    def __str__(self):
        return f"{self.material} → {self.cajonera_destino}"


class Baja(models.Model):
    """Retiro definitivo de un elemento (uno a uno con material)."""

    id = models.AutoField(primary_key=True, db_column="id_baja")
    material = models.OneToOneField(Material, on_delete=models.RESTRICT, db_column="id_material", related_name="baja")
    usuario = models.ForeignKey("accesos.Usuario", on_delete=models.RESTRICT, db_column="id_usuario",
                                related_name="bajas")
    fecha = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=200)
    destino_final = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "baja"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Baja de {self.material}"
