"""
Carga masiva de material desde CSV o XLSX (CU-B1, curso alternativo 3.a).

Cada fila se valida con las mismas reglas del formulario. Las válidas se
registran (cada una en su propia transacción) y las rechazadas se informan
con su número de fila y el motivo.

Para migrar el inventario anterior, la carga puede crear las categorías,
unidades (carros) y cajoneras que aún no existan. Los nombres se comparan sin
distinguir mayúsculas, tildes ni espacios repetidos, para no duplicar catálogos.
Si una fila se rechaza, los catálogos creados por ella se deshacen.
"""
import csv
import io
import re
import unicodedata
from dataclasses import dataclass, field

from django.core.exceptions import ValidationError
from django.db import transaction

from accesos import auditoria
from nucleo.enums import AccionAuditoria, TipoMaterial, TipoUnidad

from . import services
from .models import Cajonera, Categoria, Unidad

COLUMNAS = ["codigo_institucional", "nombre", "categoria", "unidad", "cajonera", "tipo", "cantidad",
            "marca", "modelo", "numero_serie", "observaciones"]
OBLIGATORIAS = ["nombre", "categoria", "unidad", "cajonera", "tipo"]
SINONIMOS = {"codigo": "codigo_institucional", "serie": "numero_serie", "n_serie": "numero_serie",
             "numero_de_serie": "numero_serie", "ubicacion": "cajonera", "carro": "unidad"}

LARGO_CATEGORIA = Categoria._meta.get_field("nombre").max_length
LARGO_UNIDAD = Unidad._meta.get_field("codigo").max_length
LARGO_CAJONERA = Cajonera._meta.get_field("nombre").max_length


@dataclass
class ResultadoImportacion:
    registrados: list = field(default_factory=list)
    rechazados: list = field(default_factory=list)
    categorias_creadas: list = field(default_factory=list)
    unidades_creadas: list = field(default_factory=list)
    cajoneras_creadas: list = field(default_factory=list)

    @property
    def total(self):
        return len(self.registrados) + len(self.rechazados)

    @property
    def catalogos_creados(self):
        return len(self.categorias_creadas) + len(self.unidades_creadas) + len(self.cajoneras_creadas)


def clave(texto):
    """«  Cabina  Tripulación » y «CABINA TRIPULACION» son la misma cajonera."""
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", texto).strip().lower()


def _limpio(texto):
    return re.sub(r"\s+", " ", str(texto or "")).strip()


class Catalogos:
    """Busca (y opcionalmente crea) categorías, unidades y cajoneras con caché en memoria."""

    def __init__(self, crear, usuario, resultado):
        self.crear, self.usuario, self.resultado = crear, usuario, resultado
        self.categorias = {clave(c.nombre): c for c in Categoria.objects.all()}
        self.unidades = {}
        for u in Unidad.objects.all():
            self.unidades.setdefault(clave(u.codigo), u)
        for u in Unidad.objects.all():  # también por nombre, si no choca con un código
            self.unidades.setdefault(clave(u.nombre), u)
        self.cajoneras = {(c.unidad_id, clave(c.nombre)): c for c in Cajonera.objects.all()}
        self._fila = []

    # Una fila rechazada deshace sus catálogos en la base (transacción) y aquí (caché).
    def iniciar_fila(self):
        self._fila = []

    def deshacer_fila(self):
        for diccionario, llave, lista, texto in self._fila:
            diccionario.pop(llave, None)
            lista.remove(texto)
        self._fila = []

    def _registrar(self, diccionario, llave, objeto, lista, texto, entidad):
        diccionario[llave] = objeto
        lista.append(texto)
        self._fila.append((diccionario, llave, lista, texto))
        auditoria.registrar(AccionAuditoria.ALTA, entidad, objeto.pk, nuevos=auditoria.instantanea(objeto),
                            usuario=self.usuario)

    def categoria(self, nombre, errores):
        existente = self.categorias.get(clave(nombre))
        if existente or not self.crear:
            if not existente:
                errores.append(f"la categoría «{nombre}» no existe")
            return existente
        nombre = _limpio(nombre)
        if len(nombre) > LARGO_CATEGORIA:
            errores.append(f"el nombre de la categoría supera {LARGO_CATEGORIA} caracteres")
            return None
        nueva = Categoria.objects.create(nombre=nombre)
        self._registrar(self.categorias, clave(nombre), nueva, self.resultado.categorias_creadas, nombre,
                        "categoria")
        return nueva

    def unidad(self, codigo, errores):
        existente = self.unidades.get(clave(codigo))
        if existente or not self.crear:
            return existente  # sin crear, el error se informa como cajonera inexistente
        codigo = _limpio(codigo).upper()
        if len(codigo) > LARGO_UNIDAD:
            errores.append(f"el código de la unidad «{codigo}» supera {LARGO_UNIDAD} caracteres")
            return None
        tipo = TipoUnidad.BODEGA if clave(codigo).startswith("bod") else TipoUnidad.CARRO
        nueva = Unidad.objects.create(codigo=codigo, nombre=codigo, tipo=tipo)
        self._registrar(self.unidades, clave(codigo), nueva, self.resultado.unidades_creadas, codigo, "unidad")
        return nueva

    def cajonera(self, unidad, nombre, errores):
        llave = (unidad.pk, clave(nombre))
        existente = self.cajoneras.get(llave)
        if existente or not self.crear:
            if not existente:
                errores.append(f"la cajonera «{unidad.codigo} / {nombre}» no existe")
            return existente
        nombre = _limpio(nombre)
        if len(nombre) > LARGO_CAJONERA:
            errores.append(f"el nombre de la cajonera supera {LARGO_CAJONERA} caracteres")
            return None
        nueva = Cajonera.objects.create(unidad=unidad, nombre=nombre)
        self._registrar(self.cajoneras, llave, nueva, self.resultado.cajoneras_creadas,
                        f"{unidad.codigo} / {nombre}", "cajonera")
        return nueva


def _normalizar_encabezado(texto):
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    texto = texto.strip().lower().replace(" ", "_").replace(".", "")
    return SINONIMOS.get(texto, texto)


def _leer_csv(contenido):
    texto = contenido.decode("utf-8-sig", errors="replace")
    try:
        dialecto = csv.Sniffer().sniff(texto.splitlines()[0] if texto else "", delimiters=";,\t")
    except csv.Error:
        dialecto = csv.excel
    return list(csv.reader(io.StringIO(texto), dialecto))


def _leer_xlsx(contenido):
    from openpyxl import load_workbook

    libro = load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
    hoja = libro.active
    return [["" if c is None else str(c) for c in fila] for fila in hoja.iter_rows(values_only=True)]


def leer_filas(archivo):
    nombre = (getattr(archivo, "name", "") or "").lower()
    contenido = archivo.read()
    if nombre.endswith(".xlsx"):
        try:
            return _leer_xlsx(contenido)
        except Exception as exc:  # openpyxl lanza varios tipos según el daño del archivo
            raise ValidationError("No se pudo leer la planilla XLSX.") from exc
    if nombre.endswith(".csv"):
        return _leer_csv(contenido)
    raise ValidationError("Formato no admitido: adjunte una planilla CSV o XLSX.")


def _validar_basicos(fila):
    errores = [f"falta «{columna}»" for columna in OBLIGATORIAS if not fila.get(columna)]
    if errores:
        return None, None, errores
    tipo = fila["tipo"].strip().lower()
    if tipo not in TipoMaterial.values:
        errores.append("el tipo debe ser «unitario» o «granel»")
    cantidad = 1
    if fila.get("cantidad"):
        try:
            cantidad = int(float(fila["cantidad"].replace(",", ".")))
            if cantidad < 1:
                raise ValueError
        except ValueError:
            errores.append("la cantidad debe ser un entero mayor o igual a 1")
    return tipo, cantidad, errores


def _fila_a_datos(fila, catalogos):
    tipo, cantidad, errores = _validar_basicos(fila)
    if errores:
        return None, errores
    categoria = catalogos.categoria(fila["categoria"], errores)
    unidad = catalogos.unidad(fila["unidad"], errores)
    cajonera = catalogos.cajonera(unidad, fila["cajonera"], errores) if unidad else None
    if unidad is None and not catalogos.crear:
        errores.append(f"la cajonera «{fila['unidad']} / {fila['cajonera']}» no existe")
    if errores:
        return None, errores
    datos = {
        "codigo_institucional": fila.get("codigo_institucional") or None,
        "nombre": fila["nombre"][:100],
        "categoria": categoria,
        "cajonera": cajonera,
        "tipo": tipo,
        "cantidad": cantidad,
        "marca": (fila.get("marca") or None),
        "modelo": (fila.get("modelo") or None),
        "numero_serie": (fila.get("numero_serie") or None),
        "observaciones": (fila.get("observaciones") or None),
    }
    return datos, []


class _FilaRechazada(Exception):
    def __init__(self, motivos):
        self.motivos = motivos


def importar_planilla(archivo, usuario, crear_catalogos=True):
    filas = leer_filas(archivo)
    if not filas:
        raise ValidationError("La planilla está vacía.")
    encabezados = [_normalizar_encabezado(c) for c in filas[0]]
    faltantes = [c for c in OBLIGATORIAS if c not in encabezados]
    if faltantes:
        raise ValidationError("Faltan columnas obligatorias: " + ", ".join(faltantes) + ".")

    resultado = ResultadoImportacion()
    catalogos = Catalogos(crear_catalogos, usuario, resultado)
    for numero, valores in enumerate(filas[1:], start=2):
        fila = {encabezados[i]: str(v).strip() for i, v in enumerate(valores) if i < len(encabezados)}
        if not any(fila.values()):
            continue
        catalogos.iniciar_fila()
        try:
            with transaction.atomic():
                datos, errores = _fila_a_datos(fila, catalogos)
                if errores:
                    raise _FilaRechazada(errores)
                try:
                    material = services.registrar_material(datos, usuario)
                except ValidationError as error:
                    raise _FilaRechazada(error.messages) from error
        except _FilaRechazada as rechazo:
            catalogos.deshacer_fila()
            resultado.rechazados.append({"fila": numero, "nombre": fila.get("nombre", ""),
                                         "motivos": rechazo.motivos})
            continue
        resultado.registrados.append(material)
    return resultado


def plantilla_csv():
    ejemplo = ["8C-0999", "Motobomba portátil", "MOTORES", "B-8", "Cabina trasera", "unitario", "1",
               "Honda", "WX15", "", "Ejemplo: borre esta fila"]
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";")
    escritor.writerow(COLUMNAS)
    escritor.writerow(ejemplo)
    return "﻿" + salida.getvalue()
