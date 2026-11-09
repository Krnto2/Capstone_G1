"""
Restaura un respaldo .zip de SIREMA desde la consola (cuando la web no está disponible).

    python manage.py restaurar_respaldo /ruta/sirema_20261108_030000.zip

Antes de restaurar guarda una copia de seguridad del estado actual en respaldos/manuales.
"""
from pathlib import Path

from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand, CommandError

from nucleo import respaldos


class Command(BaseCommand):
    help = "Reemplaza la base de datos y las fotografías por las de un respaldo .zip."

    def add_arguments(self, parser):
        parser.add_argument("archivo")
        parser.add_argument("--sin-copia", action="store_true",
                            help="No guardar una copia del estado actual antes de restaurar.")
        parser.add_argument("--si", action="store_true", help="No pedir confirmación.")

    def handle(self, archivo, sin_copia=False, si=False, **opciones):
        ruta = Path(archivo)
        if not ruta.is_file():
            raise CommandError(f"No existe el archivo {ruta}.")
        try:
            manifiesto = respaldos.leer_manifiesto(ruta)
        except respaldos.ErrorRespaldo as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(f"Respaldo del {manifiesto['creado']} (SIREMA {manifiesto['version']}).")
        if not si and input("Se reemplazarán TODOS los datos actuales. Escriba RESTAURAR: ") != "RESTAURAR":
            raise CommandError("Cancelado.")
        try:
            if not sin_copia:
                copia = respaldos.crear_respaldo("manuales", "antes_de_restaurar")
                self.stdout.write(f"Copia del estado actual: {copia}")
            respaldos.restaurar(ruta)
        except respaldos.ErrorRespaldo as exc:
            raise CommandError(str(exc)) from exc
        Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Restauración completa. Todas las sesiones se cerraron."))
