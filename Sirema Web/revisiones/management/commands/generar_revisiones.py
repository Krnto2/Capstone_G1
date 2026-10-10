"""
CU-C4 Generar revisiones programadas (patrón comando).

cron lo ejecuta a diario en sirema-scheduler; también puede lanzarse a mano:
    python manage.py generar_revisiones [--fecha 2026-10-09]
"""
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from revisiones.programador import ProgramadorRevisiones


class Command(BaseCommand):
    help = "Genera las revisiones del día, marca las vencidas y emite los avisos (idempotente)."

    def add_arguments(self, parser):
        parser.add_argument("--fecha", help="Fecha de referencia AAAA-MM-DD (por defecto, hoy).")

    def handle(self, *args, **opciones):
        fecha = None
        if opciones["fecha"]:
            try:
                fecha = date.fromisoformat(opciones["fecha"])
            except ValueError as error:
                raise CommandError("Use el formato AAAA-MM-DD.") from error
        resumen = ProgramadorRevisiones(fecha=fecha).ejecutar()
        self.stdout.write(self.style.SUCCESS(f"Programador: {resumen}."))
