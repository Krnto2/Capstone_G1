"""
Servicio de almacenamiento local de fotografías (actor secundario de CU-C10).

Fachada (DAS 3.3): oculta la validación, el redimensionado, el cálculo del hash
SHA-256 y la escritura del archivo. Las imágenes se guardan fuera de la base de
datos, en el volumen media, y se identifican por un UUID no predecible.
"""
import hashlib
import io
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from PIL import Image, ImageOps, UnidentifiedImageError

FORMATOS_ACEPTADOS = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}


class ErrorAlmacenamiento(Exception):
    pass


@dataclass
class ArchivoGuardado:
    id: uuid.UUID
    ruta: str
    hash_sha256: str
    tamano_bytes: int
    tipo_mime: str
    nombre_archivo: str
    fecha_hora_captura: datetime
    latitud: Decimal | None
    longitud: Decimal | None


def _sha256(contenido):
    return hashlib.sha256(contenido).hexdigest()


def _fecha_exif(exif):
    try:
        bruto = exif.get_ifd(0x8769).get(36867) or exif.get(306)
        if not bruto:
            return None
        fecha = datetime.strptime(str(bruto).strip("\x00 "), "%Y:%m:%d %H:%M:%S")
        return timezone.make_aware(fecha)
    except (ValueError, TypeError, KeyError, OverflowError):
        return None


def _coordenada(valor, referencia):
    grados, minutos, segundos = (float(v) for v in valor)
    decimal = grados + minutos / 60 + segundos / 3600
    if referencia in ("S", "W"):
        decimal = -decimal
    return Decimal(str(round(decimal, 6)))


def _gps_exif(exif):
    try:
        gps = exif.get_ifd(0x8825)
        if 2 in gps and 4 in gps:
            return _coordenada(gps[2], gps.get(1, "N")), _coordenada(gps[4], gps.get(3, "E"))
    except (ValueError, TypeError, ZeroDivisionError, KeyError):
        pass
    return None, None


class ServicioAlmacenamiento:
    """IAlmacenamiento: guardar(archivo) y verificar(foto)."""

    def __init__(self, raiz=None):
        self.raiz = Path(raiz or settings.MEDIA_ROOT)

    def ruta_absoluta(self, ruta_relativa):
        ruta = (self.raiz / ruta_relativa).resolve()
        if self.raiz.resolve() not in ruta.parents:
            raise ErrorAlmacenamiento("Ruta de archivo no válida.")
        return ruta

    def guardar(self, archivo, subcarpeta="fotografias"):
        """Valida, redimensiona a 1 MB como máximo, calcula el hash y escribe."""
        tamano = getattr(archivo, "size", None)
        if tamano is not None and tamano > settings.SIREMA_FOTO_MAX_BYTES:
            raise ErrorAlmacenamiento("La fotografía supera los 10 MB permitidos.")
        contenido = archivo.read()
        if not contenido:
            raise ErrorAlmacenamiento("El archivo está vacío.")
        if len(contenido) > settings.SIREMA_FOTO_MAX_BYTES:
            raise ErrorAlmacenamiento("La fotografía supera los 10 MB permitidos.")

        try:
            imagen = Image.open(io.BytesIO(contenido))
            formato = imagen.format
            imagen.load()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise ErrorAlmacenamiento("El archivo no es una imagen válida.") from exc
        if formato not in FORMATOS_ACEPTADOS:
            raise ErrorAlmacenamiento("Formato no admitido: use JPEG, PNG o WebP.")

        exif = imagen.getexif()
        ahora = timezone.now()
        captura = _fecha_exif(exif)
        if captura is None or captura > ahora:
            captura = ahora
        latitud, longitud = _gps_exif(exif)

        salida = self._redimensionar(imagen)
        identificador = uuid.uuid4()
        relativa = Path(subcarpeta) / f"{ahora:%Y}" / f"{ahora:%m}" / f"{identificador}.jpg"
        destino = self.raiz / relativa
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(salida)

        nombre = Path(getattr(archivo, "name", "") or f"{identificador}.jpg").name[:150]
        return ArchivoGuardado(
            id=identificador,
            ruta=relativa.as_posix(),
            hash_sha256=_sha256(salida),
            tamano_bytes=len(salida),
            tipo_mime="image/jpeg",
            nombre_archivo=nombre,
            fecha_hora_captura=captura,
            latitud=latitud,
            longitud=longitud,
        )

    def _redimensionar(self, imagen):
        imagen = ImageOps.exif_transpose(imagen)
        if imagen.mode in ("RGBA", "LA", "P"):
            imagen = imagen.convert("RGBA")
            fondo = Image.new("RGB", imagen.size, (255, 255, 255))
            fondo.paste(imagen, mask=imagen.split()[-1])
            imagen = fondo
        elif imagen.mode != "RGB":
            imagen = imagen.convert("RGB")

        lado = settings.SIREMA_FOTO_LADO_MAXIMO
        limite = settings.SIREMA_FOTO_SALIDA_MAX_BYTES
        calidad = 85
        while True:
            copia = imagen.copy()
            copia.thumbnail((lado, lado), Image.Resampling.LANCZOS)
            bufer = io.BytesIO()
            copia.save(bufer, "JPEG", quality=calidad, optimize=True)
            datos = bufer.getvalue()
            if len(datos) <= limite or (lado <= 640 and calidad <= 50):
                return datos
            if calidad > 60:
                calidad -= 10
            else:
                lado = int(lado * 0.8)

    def leer(self, ruta_relativa):
        return self.ruta_absoluta(ruta_relativa).read_bytes()

    def eliminar(self, ruta_relativa):
        """Borra un archivo del volumen media. No falla si ya no existe."""
        if not ruta_relativa:
            return
        try:
            self.ruta_absoluta(ruta_relativa).unlink(missing_ok=True)
        except (OSError, ErrorAlmacenamiento):
            pass

    def verificar(self, foto):
        """True si el archivo existe y su hash coincide con el registrado."""
        try:
            return _sha256(self.leer(foto.ruta_almacenamiento)) == foto.hash_sha256
        except (OSError, ErrorAlmacenamiento):
            return False
