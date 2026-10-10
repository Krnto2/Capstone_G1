"""
ServicioReportes: indicadores del panel de cumplimiento (RF-09, CU-C14).

% de cumplimiento = revisiones realizadas en plazo / revisiones con fecha
límite en el período. Se consideran las revisiones ya exigibles (fecha límite
pasada o realizadas); las que aún están dentro de plazo no penalizan, y las
no realizadas por baja del elemento no cuentan.
"""
from collections import Counter
from dataclasses import dataclass, field

from django.db.models import F, Q

from inventario.models import Categoria, Material, Unidad
from nucleo.enums import CriticidadHallazgo, EstadoHallazgo, EstadoRevision
from nucleo.utilidades import hoy, inicio_fin_mes, nombre_mes
from revisiones.models import Hallazgo, Revision


@dataclass
class Filtros:
    anio: int
    mes: int
    unidad: Unidad | None = None
    categoria: Categoria | None = None

    @classmethod
    def desde_parametros(cls, parametros):
        actual = hoy()
        anio, mes = actual.year, actual.month
        periodo = (parametros.get("periodo") or "").strip()
        if periodo:
            try:
                a, m = (int(x) for x in periodo.split("-")[:2])
                if 1 <= m <= 12 and 2000 <= a <= 2100:
                    anio, mes = a, m
            except ValueError:
                pass
        unidad = Unidad.objects.filter(pk=parametros.get("unidad")).first() if \
            str(parametros.get("unidad", "")).isdigit() else None
        categoria = Categoria.objects.filter(pk=parametros.get("categoria")).first() if \
            str(parametros.get("categoria", "")).isdigit() else None
        return cls(anio, mes, unidad, categoria)

    @property
    def inicio(self):
        return inicio_fin_mes(self.anio, self.mes)[0]

    @property
    def fin(self):
        return inicio_fin_mes(self.anio, self.mes)[1]

    @property
    def periodo(self):
        return f"{self.anio:04d}-{self.mes:02d}"

    @property
    def etiqueta(self):
        partes = [nombre_mes(self.anio, self.mes)]
        partes.append(f"Unidad {self.unidad.codigo}" if self.unidad else "Todas las unidades")
        partes.append(f"Categoría {self.categoria.nombre}" if self.categoria else "Todas las categorías")
        return " · ".join(partes)

    def como_parametros(self):
        datos = {"periodo": self.periodo}
        if self.unidad:
            datos["unidad"] = self.unidad.pk
        if self.categoria:
            datos["categoria"] = self.categoria.pk
        return datos


@dataclass
class FilaCumplimiento:
    etiqueta: str
    exigibles: int
    en_plazo: int

    @property
    def porcentaje(self):
        return round(self.en_plazo * 100 / self.exigibles, 1) if self.exigibles else None


@dataclass
class Indicadores:
    filtros: Filtros
    exigibles: int = 0
    en_plazo: int = 0
    fuera_de_plazo: int = 0
    vencidas: list = field(default_factory=list)
    vencidas_por_unidad: dict = field(default_factory=dict)
    hallazgos_abiertos: list = field(default_factory=list)
    hallazgos_alta: int = 0
    sin_plan: int = 0
    total_activos: int = 0
    por_unidad: list = field(default_factory=list)
    por_categoria: list = field(default_factory=list)
    total_periodo: int = 0

    @property
    def porcentaje(self):
        return round(self.en_plazo * 100 / self.exigibles, 1) if self.exigibles else None

    @property
    def detalle_vencidas(self):
        return " · ".join(f"{n} en {codigo}" for codigo, n in self.vencidas_por_unidad.items())


class ServicioReportes:
    def __init__(self, filtros):
        self.filtros = filtros

    def _filtrar_material(self, consulta, prefijo):
        if self.filtros.unidad:
            consulta = consulta.filter(**{f"{prefijo}cajonera__unidad": self.filtros.unidad})
        if self.filtros.categoria:
            consulta = consulta.filter(**{f"{prefijo}categoria": self.filtros.categoria})
        return consulta

    def revisiones_periodo(self):
        revisiones = Revision.objects.completa().filter(
            fecha_limite__range=(self.filtros.inicio, self.filtros.fin)).exclude(estado=EstadoRevision.NO_REALIZADA)
        return self._filtrar_material(revisiones, "asignacion__material__")

    @staticmethod
    def _exigibles(revisiones):
        return revisiones.filter(Q(fecha_limite__lt=hoy()) | Q(estado=EstadoRevision.REALIZADA))

    @staticmethod
    def _en_plazo(revisiones):
        return revisiones.filter(estado=EstadoRevision.REALIZADA, fecha_hora_termino__date__lte=F("fecha_limite"))

    def cumplimiento(self):
        revisiones = self.revisiones_periodo()
        exigibles = self._exigibles(revisiones)
        ind = Indicadores(filtros=self.filtros)
        ind.total_periodo = revisiones.count()
        ind.exigibles = exigibles.count()
        ind.en_plazo = self._en_plazo(exigibles).count()
        ind.fuera_de_plazo = exigibles.filter(estado=EstadoRevision.REALIZADA).count() - ind.en_plazo
        ind.vencidas = list(revisiones.filter(estado=EstadoRevision.VENCIDA).order_by("fecha_limite"))
        ind.vencidas_por_unidad = dict(Counter(r.material.cajonera.unidad.codigo for r in ind.vencidas))

        hallazgos = self._filtrar_material(
            Hallazgo.objects.exclude(estado=EstadoHallazgo.CERRADO).select_related(
                "revision__asignacion__material__cajonera__unidad"), "revision__asignacion__material__")
        ind.hallazgos_abiertos = list(hallazgos.order_by("criticidad", "-fecha_apertura"))
        orden = {CriticidadHallazgo.ALTA: 0, CriticidadHallazgo.MEDIA: 1, CriticidadHallazgo.BAJA: 2}
        ind.hallazgos_abiertos.sort(key=lambda h: (orden.get(h.criticidad, 9), -h.fecha_apertura.timestamp()))
        ind.hallazgos_alta = sum(1 for h in ind.hallazgos_abiertos if h.criticidad == CriticidadHallazgo.ALTA)

        activos = self._filtrar_material(Material.objects.activos(), "")
        ind.total_activos = activos.count()
        ind.sin_plan = activos.exclude(asignaciones__activa=True).count()

        unidades = [self.filtros.unidad] if self.filtros.unidad else Unidad.objects.filter(activo=True)
        for unidad in unidades:
            de_unidad = exigibles.filter(asignacion__material__cajonera__unidad=unidad)
            fila = FilaCumplimiento(str(unidad), de_unidad.count(), self._en_plazo(de_unidad).count())
            if fila.exigibles:
                ind.por_unidad.append(fila)
        categorias = [self.filtros.categoria] if self.filtros.categoria else Categoria.objects.all()
        for categoria in categorias:
            de_categoria = exigibles.filter(asignacion__material__categoria=categoria)
            fila = FilaCumplimiento(categoria.nombre, de_categoria.count(), self._en_plazo(de_categoria).count())
            if fila.exigibles:
                ind.por_categoria.append(fila)
        return ind

    def detalle(self):
        return self.revisiones_periodo().order_by("fecha_limite", "asignacion__material__codigo_institucional")
