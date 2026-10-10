"""
Crea el primer administrador del sistema.

Uso:
    python manage.py crear_administrador --correo admin@octava.cl --rut 11.111.111-1 \
        --nombre Ana --apellidos Pérez --contrasena Clave1234
Sin argumentos toma SIREMA_ADMIN_CORREO, SIREMA_ADMIN_RUT, SIREMA_ADMIN_CONTRASENA
del entorno (lo usa el contenedor en su primer arranque). Si ya existe un
administrador activo no hace nada.
"""
import os

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from accesos.models import Rol, Usuario
from nucleo.utilidades import formatear_rut, rut_valido


class Command(BaseCommand):
    help = "Crea el primer administrador de SIREMA si aún no existe."

    def add_arguments(self, parser):
        parser.add_argument("--correo", default=os.environ.get("SIREMA_ADMIN_CORREO"))
        parser.add_argument("--rut", default=os.environ.get("SIREMA_ADMIN_RUT"))
        parser.add_argument("--nombre", default=os.environ.get("SIREMA_ADMIN_NOMBRE", "Administrador"))
        parser.add_argument("--apellidos", default=os.environ.get("SIREMA_ADMIN_APELLIDOS", "SIREMA"))
        parser.add_argument("--contrasena", default=os.environ.get("SIREMA_ADMIN_CONTRASENA"))

    def handle(self, *args, **opciones):
        if Usuario.objects.activos().filter(rol__nombre=Rol.ADMINISTRADOR).exists():
            self.stdout.write("Ya existe un administrador activo; no se crea otro.")
            return
        correo, rut, contrasena = opciones["correo"], opciones["rut"], opciones["contrasena"]
        if not (correo and rut and contrasena):
            self.stdout.write(self.style.WARNING(
                "No hay administrador. Defina SIREMA_ADMIN_CORREO, SIREMA_ADMIN_RUT y "
                "SIREMA_ADMIN_CONTRASENA o use los argumentos --correo, --rut y --contrasena."))
            return
        if not rut_valido(rut):
            raise CommandError("El RUT del administrador no es válido.")
        usuario = Usuario(correo=correo.lower(), rut=formatear_rut(rut), nombre=opciones["nombre"],
                          apellidos=opciones["apellidos"], rol=Rol.objects.get(nombre=Rol.ADMINISTRADOR))
        try:
            password_validation.validate_password(contrasena, usuario)
        except ValidationError as error:
            raise CommandError(" ".join(error.messages)) from error
        usuario.set_password(contrasena)
        usuario.save()
        self.stdout.write(self.style.SUCCESS(f"Administrador {usuario.correo} creado."))
