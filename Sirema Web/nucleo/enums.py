"""
Tipos enumerados del modelo relacional (sección 3).

Se implementan como columnas de texto con una restricción CHECK por columna
(ver `restriccion_enum`), que da la misma garantía de integridad que un ENUM de
PostgreSQL y es compatible con las migraciones de Django.
"""
from django.db import models
from django.db.models import Q


class TipoUnidad(models.TextChoices):
    CARRO = "carro", "Carro"
    BODEGA = "bodega", "Bodega"


class TipoMaterial(models.TextChoices):
    UNITARIO = "unitario", "Unitario"
    GRANEL = "granel", "Granel"


class EstadoMaterial(models.TextChoices):
    ACTIVO = "activo", "Activo"
    DE_BAJA = "de_baja", "De baja"


class UnidadFrecuencia(models.TextChoices):
    DIA = "dia", "Día(s)"
    SEMANA = "semana", "Semana(s)"
    MES = "mes", "Mes(es)"
    ANIO = "anio", "Año(s)"


class TipoDatoPunto(models.TextChoices):
    BOOLEANO = "booleano", "Sí / No"
    NUMERICO = "numerico", "Valor medido"
    TEXTO = "texto", "Texto"
    SELECCION = "seleccion", "Solo resultado"


class EstadoRevision(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    EN_CURSO = "en_curso", "En curso"
    REALIZADA = "realizada", "Realizada"
    VENCIDA = "vencida", "Vencida"
    NO_REALIZADA = "no_realizada", "No realizada"


class ResultadoControl(models.TextChoices):
    CONFORME = "conforme", "Conforme"
    OBSERVACION = "observacion", "Observación"
    FALLA = "falla", "Falla"


class CriticidadHallazgo(models.TextChoices):
    ALTA = "alta", "Alta"
    MEDIA = "media", "Media"
    BAJA = "baja", "Baja"


class EstadoHallazgo(models.TextChoices):
    ABIERTO = "abierto", "Abierto"
    EN_REPARACION = "en_reparacion", "En reparación"
    CERRADO = "cerrado", "Cerrado"


class TipoNotificacion(models.TextChoices):
    ASIGNACION = "asignacion", "Asignación"
    RECORDATORIO = "recordatorio", "Recordatorio"
    VENCIMIENTO = "vencimiento", "Vencimiento"
    HALLAZGO = "hallazgo", "Hallazgo"


class AccionAuditoria(models.TextChoices):
    ALTA = "alta", "Alta"
    MODIFICACION = "modificacion", "Modificación"
    BAJA = "baja", "Baja"
    MOVIMIENTO = "movimiento", "Movimiento"
    REVISION = "revision", "Revisión"
    ACCESO = "acceso", "Acceso"


def restriccion_enum(campo, enumeracion, nombre, nulo=False):
    """CHECK que limita `campo` a los valores de `enumeracion`."""
    condicion = Q(**{f"{campo}__in": enumeracion.values})
    if nulo:
        condicion |= Q(**{f"{campo}__isnull": True})
    return models.CheckConstraint(condition=condicion, name=nombre)
