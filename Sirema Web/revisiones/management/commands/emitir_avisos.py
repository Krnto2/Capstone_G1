"""CU-C5 Emitir notificación de vencimiento: marca vencidas y emite avisos."""
from django.core.management.base import BaseCommand

from revisiones.programador import ProgramadorRevisiones


class Command(BaseCommand):
    help = "Marca las revisiones vencidas y emite los avisos de 24 horas y de vencimiento."

    def handle(self, *args, **opciones):
        programador = ProgramadorRevisiones()
        vencidas = programador.marcar_vencidas()
        avisos = programador.emitir_avisos()
        self.stdout.write(self.style.SUCCESS(f"{vencidas} revisiones vencidas, {avisos} avisos emitidos."))
