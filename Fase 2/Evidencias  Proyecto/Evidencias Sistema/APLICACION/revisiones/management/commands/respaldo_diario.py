import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from nucleo import respaldos


class Command(BaseCommand):
    help = "Genera el respaldo diario (base + fotografías) y aplica la rotación 30/12."

    def handle(self, *args, **opciones):
        try:
            destino = respaldos.crear_respaldo("diarios")
        except respaldos.ErrorRespaldo as exc:
            raise CommandError(str(exc)) from exc
        if timezone.localdate().day == 1:
            mensuales = destino.parent.parent / "mensuales"
            mensuales.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destino, mensuales / destino.name)
        respaldos.rotar("diarios", settings.SIREMA_RESPALDOS_DIARIOS)
        respaldos.rotar("mensuales", settings.SIREMA_RESPALDOS_MENSUALES)
        self.stdout.write(self.style.SUCCESS(f"Respaldo generado en {destino}"))
