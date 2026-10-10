"""
ServicioRevisiones: coordina los casos de uso de la cadena principal.

Cada caso de uso se concentra aquí, independiente de la vista que lo invoca
(patrón capa de servicios). Las operaciones de varios pasos se confirman o se
revierten completas con transaction.atomic (RNF-08).
"""
from collections import Counter
from dataclasses import dataclass, field
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.utils import timezone

from accesos import auditoria
from nucleo.almacenamiento import ErrorAlmacenamiento, ServicioAlmacenamiento
from nucleo.enums import (AccionAuditoria, CriticidadHallazgo, EstadoHallazgo, EstadoRevision, ResultadoControl,
                          TipoDatoPunto, TipoNotificacion)
from nucleo.utilidades import a_decimal, hoy

from . import notificaciones
from .models import AsignacionPlan, Fotografia, Hallazgo, PlanRevision, PuntoControl, ResultadoPunto, Revision


class ErrorRevision(ValidationError):
    def __init__(self, mensaje, faltantes=None, requiere_hallazgo=False):
        super().__init__(mensaje)
        self.faltantes = faltantes
        self.requiere_hallazgo = requiere_hallazgo


@dataclass
class Faltantes:
    puntos: list = field(default_factory=list)
    fotos_puntos: list = field(default_factory=list)
    foto_general: bool = False

    @property
    def hay(self):
        return bool(self.puntos or self.fotos_puntos or self.foto_general)

    @property
    def n_fotos(self):
        return len(self.fotos_puntos) + (1 if self.foto_general else 0)

    @property
    def texto(self):
        partes = []
        if self.puntos:
            n = len(self.puntos)
            partes.append(f"{n} punto{'s' if n > 1 else ''}")
        if self.n_fotos:
            partes.append(f"{self.n_fotos} fotografía{'s' if self.n_fotos > 1 else ''}")
        if not partes:
            return "Lista para finalizar"
        verbo = "Falta" if len(self.puntos) + self.n_fotos == 1 else "Faltan"
        return f"{verbo} " + " y ".join(partes)

    def como_dict(self):
        return {"puntos": [p.pk for p in self.puntos], "fotos_puntos": [p.pk for p in self.fotos_puntos],
                "foto_general": self.foto_general, "texto": self.texto, "completa": not self.hay}


# ------------------------------------------------------------ Permisos ----

def puede_ejecutar(revision, usuario):
    if not usuario.tiene_permiso("revision.ejecutar"):
        return False
    return revision.usuario_responsable_id == usuario.pk or usuario.tiene_permiso("revision.supervisar")


def puede_ver(revision, usuario):
    return (revision.usuario_responsable_id == usuario.pk or revision.usuario_ejecutor_id == usuario.pk
            or usuario.tiene_permiso("revision.supervisar") or usuario.tiene_permiso("material.consultar"))


def _bloquear(revision):
    """Relee la revisión y la bloquea: su estado en memoria puede estar desactualizado."""
    return Revision.objects.select_for_update().select_related("asignacion").get(pk=revision.pk)


def _verificar_ejecucion(revision, usuario):
    if not revision.ejecutable:
        raise ErrorRevision("Esta revisión ya fue cerrada y no se puede modificar.")
    if not puede_ejecutar(revision, usuario):
        raise ErrorRevision("Esta revisión está asignada a otro bombero.")


# ------------------------------------------------------------ Ejecución ----

def iniciar(revision, usuario):
    """CU-C7 paso 2: marca la revisión en curso."""
    _verificar_ejecucion(revision, usuario)
    cambios = []
    if revision.fecha_hora_inicio is None:
        revision.fecha_hora_inicio = timezone.now()
        cambios.append("fecha_hora_inicio")
    if revision.estado == EstadoRevision.PENDIENTE:
        revision.estado = EstadoRevision.EN_CURSO
        cambios.append("estado")
    if cambios:
        revision.save(update_fields=cambios)
    return revision


def _normalizar_valor(punto, valor):
    texto = "" if valor is None else str(valor).strip()
    if punto.tipo_dato == TipoDatoPunto.NUMERICO:
        numero = a_decimal(texto)
        if numero is None:
            raise ErrorRevision("Ingrese el valor medido como número.")
        return f"{numero.normalize():f}"
    if punto.tipo_dato == TipoDatoPunto.BOOLEANO:
        if texto.lower() in ("si", "sí", "true", "1"):
            return "Sí"
        if texto.lower() in ("no", "false", "0"):
            return "No"
        raise ErrorRevision("Indique Sí o No.")
    if punto.tipo_dato == TipoDatoPunto.TEXTO:
        if not texto and punto.obligatorio:
            raise ErrorRevision("Escriba la respuesta del punto.")
        return texto[:100] or None
    return None


def registrar_resultado(revision, punto, usuario, resultado, valor=None, observacion=None):
    """CU-C8 (y CU-C9): guarda la respuesta de un punto en el momento en que se registra."""
    _verificar_ejecucion(revision, usuario)
    if punto.plan_id != revision.asignacion.plan_id:
        raise ErrorRevision("El punto no pertenece al plan de esta revisión.")
    if resultado not in ResultadoControl.values:
        raise ErrorRevision("Seleccione Conforme, Observación o Falla.")
    observacion = (observacion or "").strip()[:300] or None
    if resultado != ResultadoControl.CONFORME and not observacion:
        raise ErrorRevision("Una observación o falla exige un comentario.")
    valor = _normalizar_valor(punto, valor)
    with transaction.atomic():
        revision = _bloquear(revision)
        iniciar(revision, usuario)
        registro, _ = ResultadoPunto.objects.update_or_create(
            revision=revision, punto=punto,
            defaults={"resultado": resultado, "valor_registrado": valor, "observacion": observacion,
                      "fecha_hora_registro": timezone.now()},
        )
    return registro


def adjuntar_fotografia(revision, archivo, usuario, punto=None, descripcion=None, almacenamiento=None):
    """CU-C10: el servicio de almacenamiento devuelve ruta y hash SHA-256."""
    _verificar_ejecucion(revision, usuario)
    if punto is not None:
        if punto.plan_id != revision.asignacion.plan_id:
            raise ErrorRevision("El punto no pertenece al plan de esta revisión.")
        if not ResultadoPunto.objects.filter(revision=revision, punto=punto).exists():
            raise ErrorRevision("Registre primero el resultado del punto y luego adjunte la fotografía.")
    almacenamiento = almacenamiento or ServicioAlmacenamiento()
    try:
        guardado = almacenamiento.guardar(archivo)
    except ErrorAlmacenamiento as error:
        raise ErrorRevision(str(error)) from error

    def descartar():
        try:
            almacenamiento.ruta_absoluta(guardado.ruta).unlink(missing_ok=True)
        except (OSError, ErrorAlmacenamiento):
            pass

    if Fotografia.objects.filter(hash_sha256=guardado.hash_sha256).exists():
        descartar()
        raise ErrorRevision("Esta imagen ya fue cargada antes.")
    try:
        with transaction.atomic():
            revision = _bloquear(revision)
            iniciar(revision, usuario)
            foto = Fotografia.objects.create(
                id=guardado.id, revision=revision, punto=punto, usuario=usuario,
                nombre_archivo=guardado.nombre_archivo, ruta_almacenamiento=guardado.ruta,
                tipo_mime=guardado.tipo_mime, tamano_bytes=guardado.tamano_bytes,
                hash_sha256=guardado.hash_sha256, fecha_hora_captura=guardado.fecha_hora_captura,
                latitud=guardado.latitud, longitud=guardado.longitud,
                descripcion=(descripcion or "").strip()[:200] or None,
            )
            auditoria.registrar(AccionAuditoria.ALTA, "fotografia", foto.pk, usuario=usuario, nuevos={
                "id_revision": revision.pk, "id_punto": punto.pk if punto else None,
                "hash_sha256": foto.hash_sha256, "tamano_bytes": foto.tamano_bytes})
    except ErrorRevision:
        descartar()
        raise
    except IntegrityError as error:
        descartar()
        raise ErrorRevision("No se pudo registrar la fotografía.") from error
    return foto


def faltantes(revision):
    """CU-C7 paso 6: puntos obligatorios sin respuesta y fotografías exigidas."""
    puntos = list(revision.asignacion.plan.puntos.all())
    respondidos = set(revision.resultados.values_list("punto_id", flat=True))
    fotos = list(revision.fotografias.filter(anulada=False).values_list("punto_id", flat=True))
    por_punto = Counter(fotos)
    resultado = Faltantes()
    resultado.puntos = [p for p in puntos if p.obligatorio and p.pk not in respondidos]
    resultado.fotos_puntos = [p for p in puntos if p.exige_fotografia and (p.obligatorio or p.pk in respondidos)
                              and not por_punto.get(p.pk)]
    resultado.foto_general = revision.asignacion.plan.exige_fotografia and not fotos
    return resultado


def resumen(revision):
    resultados = list(revision.resultados.all())
    conteo = Counter(r.resultado for r in resultados)
    return {
        "resultado_global": revision.calcular_resultado_global(resultados),
        "respondidos": len(resultados),
        "total": revision.asignacion.plan.puntos.count(),
        "conformes": conteo.get(ResultadoControl.CONFORME, 0),
        "observaciones": conteo.get(ResultadoControl.OBSERVACION, 0),
        "fallas": conteo.get(ResultadoControl.FALLA, 0),
        "fotografias": revision.fotografias.filter(anulada=False).count(),
    }


def finalizar(revision, usuario, observaciones=None, hallazgo=None):
    """CU-C7 pasos 6 y 7, con CU-C12 si el resultado global es falla. Una sola transacción."""
    with transaction.atomic():
        revision = Revision.objects.select_for_update().select_related(
            "asignacion__plan", "asignacion__material__cajonera__unidad").get(pk=revision.pk)
        _verificar_ejecucion(revision, usuario)
        pendientes = faltantes(revision)
        if pendientes.hay:
            raise ErrorRevision(pendientes.texto + ".", faltantes=pendientes)
        resultados = list(revision.resultados.select_related("punto"))
        global_ = revision.calcular_resultado_global(resultados)

        datos_hallazgo = None
        if global_ == ResultadoControl.FALLA:
            datos_hallazgo = hallazgo or {}
            descripcion = (datos_hallazgo.get("descripcion") or "").strip()
            criticidad = datos_hallazgo.get("criticidad")
            if not descripcion or criticidad not in CriticidadHallazgo.values:
                raise ErrorRevision("Una revisión con falla no se puede finalizar sin describir el hallazgo "
                                    "y su criticidad.", requiere_hallazgo=True)

        ahora = timezone.now()
        revision.estado = EstadoRevision.REALIZADA
        revision.usuario_ejecutor = usuario
        revision.fecha_hora_inicio = revision.fecha_hora_inicio or ahora
        revision.fecha_hora_termino = ahora
        revision.resultado_global = global_
        revision.observaciones = (observaciones or "").strip()[:500] or None
        revision.save()

        nuevo_hallazgo = None
        if datos_hallazgo is not None:
            nuevo_hallazgo = Hallazgo.objects.create(revision=revision, descripcion=descripcion[:500],
                                                     criticidad=criticidad)
            auditoria.registrar(AccionAuditoria.ALTA, "hallazgo", nuevo_hallazgo.pk, usuario=usuario,
                                nuevos=auditoria.instantanea(nuevo_hallazgo))
            notificaciones.notificar_jefatura(
                TipoNotificacion.HALLAZGO,
                f"Hallazgo de criticidad {nuevo_hallazgo.get_criticidad_display().lower()} en "
                f"{notificaciones.describir(revision)}: {descripcion}",
                revision=revision,
            )

        auditoria.registrar(AccionAuditoria.REVISION, "revision", revision.pk, usuario=usuario,
                            anteriores={"estado": EstadoRevision.EN_CURSO},
                            nuevos={
                                "estado": revision.estado,
                                "resultado_global": global_,
                                "en_plazo": revision.en_plazo,
                                "id_usuario_ejecutor": usuario.pk,
                                "resultados": [{"id_punto": r.punto_id, "resultado": r.resultado,
                                                "valor": r.valor_registrado} for r in resultados],
                                "fotografias": revision.fotografias.filter(anulada=False).count(),
                                "id_hallazgo": nuevo_hallazgo.pk if nuevo_hallazgo else None,
                            })
    return revision


def reasignar(revision, responsable, usuario):
    if not revision.ejecutable:
        raise ErrorRevision("Solo se reasignan revisiones abiertas.")
    if not responsable.activo or not responsable.tiene_permiso("revision.ejecutar"):
        raise ErrorRevision("El nuevo responsable no puede ejecutar revisiones.")
    anterior = revision.usuario_responsable_id
    with transaction.atomic():
        revision.usuario_responsable = responsable
        revision.save(update_fields=["usuario_responsable"])
        auditoria.registrar(AccionAuditoria.MODIFICACION, "revision", revision.pk,
                            {"id_usuario_responsable": anterior}, {"id_usuario_responsable": responsable.pk},
                            usuario=usuario)
        notificaciones.notificar(responsable, TipoNotificacion.ASIGNACION,
                                 f"Se le reasignó la revisión de {notificaciones.describir(revision)}, "
                                 f"fecha límite {revision.fecha_limite:%d-%m-%Y}.", revision)
    return revision


# ------------------------------------------------- Fotografías y hallazgos ----

def anular_fotografia(foto, motivo, usuario):
    """CU-C11: la imagen no se elimina; la anulación queda en la bitácora con su motivo."""
    if foto.anulada:
        raise ErrorRevision("La fotografía ya está anulada.")
    if not (motivo or "").strip():
        raise ErrorRevision("Indique el motivo de la anulación.")
    with transaction.atomic():
        foto.anulada = True
        foto.save(update_fields=["anulada"])
        auditoria.registrar(AccionAuditoria.BAJA, "fotografia", foto.pk, {"anulada": False},
                            {"anulada": True, "motivo": motivo.strip()[:300]}, usuario=usuario)
    return foto


def marcar_en_reparacion(hallazgo, usuario):
    if hallazgo.estado != EstadoHallazgo.ABIERTO:
        raise ErrorRevision("Solo un hallazgo abierto pasa a reparación.")
    with transaction.atomic():
        hallazgo.estado = EstadoHallazgo.EN_REPARACION
        hallazgo.save(update_fields=["estado"])
        auditoria.registrar(AccionAuditoria.MODIFICACION, "hallazgo", hallazgo.pk, {"estado": "abierto"},
                            {"estado": "en_reparacion"}, usuario=usuario)
    return hallazgo


def cerrar_hallazgo(hallazgo, acciones, usuario):
    """CU-C13: solo la jefatura lo cierra, registrando acción, usuario y fecha."""
    with transaction.atomic():
        estado_anterior = hallazgo.estado
        hallazgo.cerrar(acciones, usuario)
        auditoria.registrar(AccionAuditoria.MODIFICACION, "hallazgo", hallazgo.pk, {"estado": estado_anterior},
                            {"estado": "cerrado", "acciones": hallazgo.acciones}, usuario=usuario)
    return hallazgo


# -------------------------------------------------- Planes y asignaciones ----

CAMPOS_PLAN = ["nombre", "descripcion", "frecuencia_valor", "frecuencia_unidad", "dias_tolerancia",
               "exige_fotografia"]
CAMPOS_PUNTO = ["descripcion", "tipo_dato", "unidad_medida", "valor_minimo", "valor_maximo", "obligatorio",
                "exige_fotografia"]


def tiene_ejecuciones(plan):
    return (ResultadoPunto.objects.filter(punto__plan=plan).exists()
            or Revision.objects.filter(asignacion__plan=plan, estado=EstadoRevision.REALIZADA).exists())


def _crear_puntos(plan, puntos):
    for orden, datos in enumerate(puntos, start=1):
        PuntoControl.objects.create(plan=plan, numero_orden=orden, **{k: datos.get(k) for k in CAMPOS_PUNTO})


def guardar_plan(plan, datos, puntos, usuario):
    """
    CU-C1 con CU-C2. Si el plan ya tiene revisiones ejecutadas, modificarlo crea
    una versión nueva y traslada a ella las asignaciones vigentes (RF-07).
    Devuelve (plan_guardado, es_version_nueva).
    """
    if not puntos:
        raise ValidationError("El plan debe tener al menos un punto de control.")
    datos = {k: datos.get(k) for k in CAMPOS_PLAN}
    with transaction.atomic():
        if plan is None:
            version = (PlanRevision.objects.filter(nombre__iexact=datos["nombre"]).aggregate(m=Max("version"))["m"]
                       or 0) + 1
            nuevo = PlanRevision.objects.create(version=version, **datos)
            _crear_puntos(nuevo, puntos)
            auditoria.registrar(AccionAuditoria.ALTA, "plan_revision", nuevo.pk, usuario=usuario,
                                nuevos={**auditoria.instantanea(nuevo), "puntos": len(puntos)})
            return nuevo, False

        if not tiene_ejecuciones(plan):
            anteriores = auditoria.instantanea(plan)
            for campo, valor in datos.items():
                setattr(plan, campo, valor)
            plan.save()
            plan.puntos.all().delete()
            _crear_puntos(plan, puntos)
            auditoria.registrar(AccionAuditoria.MODIFICACION, "plan_revision", plan.pk, anteriores,
                                {**auditoria.instantanea(plan), "puntos": len(puntos)}, usuario=usuario)
            return plan, False

        version = max(plan.version, PlanRevision.objects.filter(nombre__iexact=datos["nombre"])
                      .aggregate(m=Max("version"))["m"] or 0) + 1
        nuevo = PlanRevision.objects.create(version=version, **datos)
        _crear_puntos(nuevo, puntos)
        plan.activo = False
        plan.save(update_fields=["activo"])
        auditoria.registrar(AccionAuditoria.ALTA, "plan_revision", nuevo.pk, usuario=usuario,
                            nuevos={**auditoria.instantanea(nuevo), "reemplaza_a": plan.pk, "puntos": len(puntos)})
        auditoria.registrar(AccionAuditoria.MODIFICACION, "plan_revision", plan.pk, {"activo": True},
                            {"activo": False, "reemplazado_por": nuevo.pk}, usuario=usuario)
        for asignacion in plan.asignaciones.filter(activa=True).select_related("material", "usuario_responsable"):
            ultima = asignacion.revisiones.aggregate(m=Max("fecha_programada"))["m"]
            inicio = nuevo.proxima_fecha(ultima) if ultima else max(asignacion.fecha_inicio, hoy())
            termino_original = asignacion.fecha_termino
            asignacion.cerrar(hoy())
            if termino_original and inicio > termino_original:
                continue
            nueva = AsignacionPlan.objects.create(plan=nuevo, material=asignacion.material,
                                                  usuario_responsable=asignacion.usuario_responsable,
                                                  fecha_inicio=inicio, fecha_termino=termino_original)
            auditoria.registrar(AccionAuditoria.ALTA, "asignacion_plan", nueva.pk, usuario=usuario,
                                nuevos={**auditoria.instantanea(nueva), "reemplaza_a": asignacion.pk})
        return nuevo, True


def desactivar_plan(plan, usuario):
    with transaction.atomic():
        plan.activo = False
        plan.save(update_fields=["activo"])
        cerradas = 0
        for asignacion in plan.asignaciones.filter(activa=True):
            asignacion.cerrar()
            cerradas += 1
        auditoria.registrar(AccionAuditoria.BAJA, "plan_revision", plan.pk, {"activo": True},
                            {"activo": False, "asignaciones_cerradas": cerradas}, usuario=usuario)
    return cerradas


def asignar_plan(plan, material, responsable, fecha_inicio, usuario, fecha_termino=None):
    """CU-C3 Asignar plan a material. Devuelve la asignación y sus primeras revisiones."""
    from .programador import ProgramadorRevisiones

    if not material.activo:
        raise ValidationError("Solo se asignan planes a elementos activos.")
    if not plan.activo or not plan.puntos.exists():
        raise ValidationError("El plan debe estar activo y tener al menos un punto de control.")
    if AsignacionPlan.objects.filter(material=material, plan=plan, activa=True).exists():
        raise ValidationError("El elemento ya tiene este plan vigente.")
    if fecha_termino and fecha_termino < fecha_inicio:
        raise ValidationError("La fecha de término no puede ser anterior a la de inicio.")
    try:
        with transaction.atomic():
            asignacion = AsignacionPlan.objects.create(plan=plan, material=material, usuario_responsable=responsable,
                                                       fecha_inicio=fecha_inicio, fecha_termino=fecha_termino)
            auditoria.registrar(AccionAuditoria.ALTA, "asignacion_plan", asignacion.pk, usuario=usuario,
                                nuevos=auditoria.instantanea(asignacion))
            notificaciones.notificar(
                responsable, TipoNotificacion.ASIGNACION,
                f"Se le asignó el plan «{plan.nombre}» ({plan.frecuencia_legible}) para {material.nombre} "
                f"({material.codigo_institucional or 's/c'}). Primera revisión: {fecha_inicio:%d-%m-%Y}.",
            )
            creadas = ProgramadorRevisiones().generar_para(asignacion)
    except IntegrityError as error:
        # El índice único parcial impide dos asignaciones activas iguales (CU-C3 5.a).
        raise ValidationError("El elemento ya tiene este plan vigente.") from error
    return asignacion, creadas


def cerrar_asignacion(asignacion, usuario):
    if not asignacion.activa:
        raise ValidationError("La asignación ya está cerrada.")
    with transaction.atomic():
        asignacion.cerrar()
        auditoria.registrar(AccionAuditoria.BAJA, "asignacion_plan", asignacion.pk, {"activa": True},
                            {"activa": False, "fecha_termino": asignacion.fecha_termino}, usuario=usuario)
    return asignacion
