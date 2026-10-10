"""
RNF-05: respaldo diario de la base de datos y de las fotografías.

Conserva 30 respaldos diarios y 12 mensuales (el del día 1 de cada mes) en el
volumen respaldos. La copia semanal al disco externo se hace desde el servidor
(ver README, sección Respaldos).
"""
import os
import shutil
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Genera el respaldo diario (pg_dump + fotografías) y aplica la rotación 30/12."

    def handle(self, *args, **opciones):
        base = Path(settings.SIREMA_RESPALDOS_DIR)
        diarios, mensuales = base / "diarios", base / "mensuales"
        diarios.mkdir(parents=True, exist_ok=True)
        mensuales.mkdir(parents=True, exist_ok=True)
        marca = datetime.now().strftime("%Y%m%d_%H%M")
        destino = diarios / marca
        destino.mkdir(exist_ok=True)

        self._respaldar_base(destino)
        self._respaldar_fotos(destino)

        if datetime.now().day == 1:
            shutil.copytree(destino, mensuales / marca, dirs_exist_ok=True)
        self._rotar(diarios, settings.SIREMA_RESPALDOS_DIARIOS)
        self._rotar(mensuales, settings.SIREMA_RESPALDOS_MENSUALES)
        self.stdout.write(self.style.SUCCESS(f"Respaldo generado en {destino}"))

    def _respaldar_base(self, destino):
        db = settings.DATABASES["default"]
        if db["ENGINE"] == "django.db.backends.postgresql":
            entorno = {**os.environ, "PGPASSWORD": db.get("PASSWORD", "")}
            comando = ["pg_dump", "-h", db["HOST"], "-p", str(db["PORT"]), "-U", db["USER"], "-Fc",
                       "-f", str(destino / "sirema.dump"), db["NAME"]]
            resultado = subprocess.run(comando, env=entorno, capture_output=True, text=True)
            if resultado.returncode != 0:
                raise CommandError(f"pg_dump falló: {resultado.stderr.strip()}")
        else:
            shutil.copy2(db["NAME"], destino / "db.sqlite3")

    def _respaldar_fotos(self, destino):
        media = Path(settings.MEDIA_ROOT)
        with tarfile.open(destino / "media.tar.gz", "w:gz") as tar:
            if media.exists():
                tar.add(media, arcname="media")

    @staticmethod
    def _rotar(carpeta, conservar):
        respaldos = sorted((p for p in carpeta.iterdir() if p.is_dir()), reverse=True)
        for viejo in respaldos[conservar:]:
            shutil.rmtree(viejo, ignore_errors=True)
