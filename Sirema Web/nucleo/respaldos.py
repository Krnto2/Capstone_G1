"""
Respaldo y restauración completos de SIREMA (RNF-05).

Un respaldo es un único archivo .zip con:

    manifiesto.json      versión, motor de base de datos, fecha y migraciones aplicadas
    base/sirema.dump     pg_dump en formato personalizado (PostgreSQL), o
    base/db.sqlite3      copia consistente de la base (SQLite, desarrollo)
    media/...            fotografías de evidencia

El mismo formato lo generan el respaldo diario (cron), el respaldo manual del
administrador y la copia de seguridad automática que se toma antes de restaurar.
Este módulo no importa modelos de las aplicaciones: trabaja a nivel de base completa.
"""
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath

from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.utils import timezone

FORMATO = 1
MANIFIESTO = "manifiesto.json"
CARPETAS = {"manuales": "Manual", "diarios": "Diario", "mensuales": "Mensual"}
NOMBRE_VALIDO = re.compile(r"sirema_\d{8}_\d{6}(_[a-z_]+)?\.zip")


class ErrorRespaldo(Exception):
    """Respaldo inválido, incompatible o que no se pudo generar o restaurar."""


@dataclass
class Respaldo:
    nombre: str
    tipo: str
    ruta: Path
    tamano: int
    fecha: datetime

    @property
    def carpeta(self):
        return self.ruta.parent.name


# ------------------------------------------------------------- Utilidades ----

def _base():
    return Path(settings.SIREMA_RESPALDOS_DIR)


def _motor():
    return connection.vendor  # "postgresql" o "sqlite"


def _db():
    return settings.DATABASES["default"]


def _entorno_pg():
    return {**os.environ, "PGPASSWORD": _db().get("PASSWORD", "") or ""}


def _args_conexion_pg():
    db = _db()
    return ["-h", db.get("HOST") or "localhost", "-p", str(db.get("PORT") or 5432), "-U", db["USER"]]


def _ejecutar(comando, **kwargs):
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, **kwargs)
    except FileNotFoundError as exc:
        raise ErrorRespaldo(f"No se encontró el programa «{comando[0]}» en el servidor.") from exc
    if resultado.returncode != 0:
        raise ErrorRespaldo(f"{comando[0]} falló: {resultado.stderr.strip()[-500:]}")
    return resultado


def migraciones_aplicadas():
    with connection.cursor() as cursor:
        cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
        return [list(fila) for fila in cursor.fetchall()]


def _miembro_seguro(nombre):
    """Rechaza rutas absolutas o con «..» dentro del zip."""
    ruta = PurePosixPath(nombre)
    return not (ruta.is_absolute() or ".." in ruta.parts or "\\" in nombre or ":" in nombre)


# ------------------------------------------------------------------ Crear ----

def crear_respaldo(carpeta="manuales", sufijo=""):
    """Genera un respaldo completo en SIREMA_RESPALDOS_DIR/<carpeta>/ y devuelve su ruta."""
    destino_dir = _base() / carpeta
    destino_dir.mkdir(parents=True, exist_ok=True)
    marca = timezone.localtime().strftime("%Y%m%d_%H%M%S")
    nombre = f"sirema_{marca}{'_' + sufijo if sufijo else ''}.zip"
    destino = destino_dir / nombre
    n = 1
    while destino.exists():  # dos respaldos en el mismo segundo
        n += 1
        destino = destino_dir / nombre.replace(".zip", f"_{'x' * (n - 1)}.zip")

    temporal = destino.with_suffix(".zip.parcial")
    with tempfile.TemporaryDirectory() as tmp:
        archivo_base = _volcar_base(Path(tmp))
        manifiesto = {
            "formato": FORMATO,
            "aplicacion": "SIREMA",
            "version": settings.SIREMA_VERSION,
            "motor": _motor(),
            "creado": timezone.localtime().isoformat(),
            "migraciones": migraciones_aplicadas(),
        }
        try:
            with zipfile.ZipFile(temporal, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
                zf.writestr(MANIFIESTO, json.dumps(manifiesto, ensure_ascii=False, indent=2))
                zf.write(archivo_base, f"base/{archivo_base.name}")
                media = Path(settings.MEDIA_ROOT)
                if media.exists():
                    for ruta in sorted(media.rglob("*")):
                        if ruta.is_file():
                            zf.write(ruta, "media/" + ruta.relative_to(media).as_posix())
        except BaseException:
            temporal.unlink(missing_ok=True)
            raise
    temporal.replace(destino)
    return destino


def _volcar_base(tmp):
    if _motor() == "postgresql":
        salida = tmp / "sirema.dump"
        _ejecutar(["pg_dump", *_args_conexion_pg(), "-Fc", "--no-owner", "-f", str(salida), _db()["NAME"]],
                  env=_entorno_pg())
        return salida
    salida = tmp / "db.sqlite3"
    connection.ensure_connection()
    destino = sqlite3.connect(salida)
    try:
        if connection.in_atomic_block:
            # backup() espera indefinidamente si el origen tiene una transacción abierta.
            destino.executescript("\n".join(connection.connection.iterdump()))
        else:
            connection.connection.backup(destino)  # copia consistente aunque haya escrituras
    finally:
        destino.close()
    return salida


# ----------------------------------------------------------------- Listar ----

def listar():
    respaldos = []
    for carpeta, tipo in CARPETAS.items():
        directorio = _base() / carpeta
        if not directorio.is_dir():
            continue
        for ruta in directorio.glob("sirema_*.zip"):
            datos = ruta.stat()
            try:
                fecha = timezone.make_aware(datetime.strptime(ruta.name[7:22], "%Y%m%d_%H%M%S"))
            except ValueError:
                fecha = datetime.fromtimestamp(datos.st_mtime, tz=timezone.get_current_timezone())
            respaldos.append(Respaldo(ruta.name, tipo, ruta, datos.st_size, fecha))
    return sorted(respaldos, key=lambda r: r.fecha, reverse=True)


def obtener(carpeta, nombre):
    """Busca un respaldo por carpeta y nombre sin permitir rutas arbitrarias."""
    if carpeta not in CARPETAS or not NOMBRE_VALIDO.fullmatch(nombre or ""):
        raise ErrorRespaldo("Respaldo no encontrado.")
    ruta = _base() / carpeta / nombre
    if not ruta.is_file():
        raise ErrorRespaldo("Respaldo no encontrado.")
    return ruta


def eliminar(carpeta, nombre):
    obtener(carpeta, nombre).unlink()


def rotar(carpeta, conservar):
    directorio = _base() / carpeta
    if not directorio.is_dir():
        return
    archivos = sorted(directorio.glob("sirema_*.zip"), key=lambda p: p.name, reverse=True)
    for viejo in archivos[conservar:]:
        viejo.unlink(missing_ok=True)
    # Formato anterior (carpetas con sirema.dump y media.tar.gz).
    carpetas = sorted((p for p in directorio.iterdir() if p.is_dir()), reverse=True)
    for vieja in carpetas[conservar:]:
        shutil.rmtree(vieja, ignore_errors=True)


# -------------------------------------------------------------- Validar ----

def leer_manifiesto(ruta):
    """Abre el zip, valida su estructura y compatibilidad, y devuelve el manifiesto."""
    try:
        zf = zipfile.ZipFile(ruta)
    except (zipfile.BadZipFile, OSError) as exc:
        raise ErrorRespaldo("El archivo no es un respaldo de SIREMA válido (no es un .zip).") from exc
    with zf:
        nombres = zf.namelist()
        if MANIFIESTO not in nombres:
            raise ErrorRespaldo("El archivo no es un respaldo de SIREMA (falta el manifiesto).")
        if not all(_miembro_seguro(n) for n in nombres):
            raise ErrorRespaldo("El respaldo contiene rutas no permitidas.")
        try:
            manifiesto = json.loads(zf.read(MANIFIESTO))
        except ValueError as exc:
            raise ErrorRespaldo("El manifiesto del respaldo está dañado.") from exc
        if manifiesto.get("aplicacion") != "SIREMA" or manifiesto.get("formato") != FORMATO:
            raise ErrorRespaldo("El archivo no es un respaldo de SIREMA compatible.")
        motor = manifiesto.get("motor")
        if motor != _motor():
            raise ErrorRespaldo(f"El respaldo es de {motor} y este servidor usa {_motor()}: no se puede restaurar aquí.")
        archivo_base = "base/sirema.dump" if motor == "postgresql" else "base/db.sqlite3"
        if archivo_base not in nombres:
            raise ErrorRespaldo("El respaldo no contiene la base de datos.")
        if zf.testzip() is not None:
            raise ErrorRespaldo("El respaldo está dañado (falla la verificación CRC).")

    conocidas = set(MigrationLoader(None, ignore_no_migrations=True).disk_migrations)
    desconocidas = {tuple(m) for m in manifiesto.get("migraciones", [])} - conocidas
    if desconocidas:
        raise ErrorRespaldo("El respaldo fue creado con una versión más nueva de SIREMA. "
                            "Actualice la aplicación antes de restaurarlo.")
    return manifiesto


# -------------------------------------------------------------- Restaurar ----

def restaurar(ruta):
    """
    Reemplaza TODA la base de datos y las fotografías por las del respaldo.

    Antes de llamar a esta función conviene tomar una copia de seguridad (la vista lo hace).
    Devuelve el manifiesto del respaldo restaurado.
    """
    manifiesto = leer_manifiesto(ruta)
    candado = _base() / ".restaurando"
    _base().mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(candado, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ErrorRespaldo("Ya hay una restauración en curso.") from exc
    os.close(descriptor)
    try:
        with tempfile.TemporaryDirectory(dir=_base()) as tmp:
            tmp = Path(tmp)
            with zipfile.ZipFile(ruta) as zf:
                zf.extractall(tmp)
            if manifiesto["motor"] == "postgresql":
                _restaurar_postgres(tmp / "base" / "sirema.dump", tmp)
            else:
                _restaurar_sqlite(tmp / "base" / "db.sqlite3")
            # Un respaldo de una versión anterior queda al día con las migraciones actuales.
            call_command("migrate", interactive=False, verbosity=0)
            _restaurar_media(tmp / "media")
    finally:
        candado.unlink(missing_ok=True)
    return manifiesto


def _restaurar_sqlite(origen):
    try:
        fuente = sqlite3.connect(f"file:{origen.as_posix()}?mode=ro", uri=True)
        tablas = {f[0] for f in fuente.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        integridad = fuente.execute("PRAGMA quick_check").fetchone()[0]
    except sqlite3.DatabaseError as exc:
        raise ErrorRespaldo("La base de datos del respaldo está dañada.") from exc
    try:
        if integridad != "ok" or not {"usuario", "django_migrations"} <= tablas:
            raise ErrorRespaldo("La base de datos del respaldo está dañada o incompleta.")
        connection.ensure_connection()
        if connection.in_atomic_block:
            raise ErrorRespaldo("No se puede restaurar dentro de una transacción.")
        fuente.backup(connection.connection)  # reemplaza la base completa, página por página
    finally:
        fuente.close()


def _restaurar_postgres(dump, tmp):
    """Borra el esquema y carga el volcado en una sola transacción: si algo falla, no cambia nada."""
    script = tmp / "restaurar.sql"
    _ejecutar(["pg_restore", "--no-owner", "--no-privileges", "-f", str(script), str(dump)])
    preparacion = tmp / "preparar.sql"
    preparacion.write_text("DROP SCHEMA IF EXISTS public CASCADE;\nCREATE SCHEMA public;\n", encoding="utf-8")
    connection.close()
    _ejecutar(["psql", *_args_conexion_pg(), "-d", _db()["NAME"], "-X", "-q", "-v", "ON_ERROR_STOP=1",
               "--single-transaction", "-f", str(preparacion), "-f", str(script)], env=_entorno_pg())
    connection.close()


def _restaurar_media(origen):
    """Reemplaza el contenido de MEDIA_ROOT (que puede ser un volumen montado)."""
    media = Path(settings.MEDIA_ROOT)
    media.mkdir(parents=True, exist_ok=True)
    for hijo in media.iterdir():
        if hijo.is_dir():
            shutil.rmtree(hijo)
        else:
            hijo.unlink()
    if origen.is_dir():
        for hijo in origen.iterdir():
            shutil.move(str(hijo), media / hijo.name)
