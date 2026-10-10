"""
Usuarios FICTICIOS de demostración (los crea `python manage.py cargar_datos_demo`).

La pantalla de inicio de sesión los muestra solo con DEBUG activo y solo si
existen en la base de datos; en producción nunca aparecen.
"""
from django.conf import settings

CONTRASENA_DEMO = "Bomberos2026"

USUARIOS_DEMO = [
    # (cuerpo del RUT, nombre, apellidos, correo, rol)
    ("11111111", "Ana", "Torres Vidal", "admin@sirema.local", "administrador"),
    ("12345678", "Carlos", "Muñoz Reyes", "jefatura@sirema.local", "jefatura"),
    ("15555555", "Juan", "Soto Pérez", "j.soto@sirema.local", "bombero"),
    ("16666666", "María", "Rivas Fuentes", "m.rivas@sirema.local", "bombero"),
    ("17777777", "Pedro", "Lagos Herrera", "p.lagos@sirema.local", "bombero"),
]


def usuarios_visibles():
    """Usuarios de demostración que existen, para mostrarlos en el ingreso (solo con DEBUG)."""
    if not settings.DEBUG:
        return []
    from .models import Usuario

    existentes = set(Usuario.objects.filter(correo__in=[u[3] for u in USUARIOS_DEMO], activo=True)
                     .values_list("correo", flat=True))
    return [{"correo": correo, "nombre": f"{nombre} {apellidos.split()[0]}", "rol": rol.capitalize()}
            for _, nombre, apellidos, correo, rol in USUARIOS_DEMO if correo in existentes]
