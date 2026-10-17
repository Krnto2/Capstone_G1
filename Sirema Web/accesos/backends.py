"""
Autenticación de SIREMA.

El ModelBackend de Django rechaza a los usuarios desactivados antes de revisar la
contraseña, y el formulario solo puede responder «correo o contraseña incorrectos».
Este backend devuelve al usuario desactivado cuando la contraseña es CORRECTA, para
que el formulario le diga que su cuenta está deshabilitada. Con una contraseña
incorrecta la respuesta sigue siendo la genérica, de modo que el formulario no
permite averiguar qué cuentas existen o están desactivadas.

get_user() se hereda sin cambios: una cuenta desactivada con la sesión abierta
pierde el acceso en su siguiente solicitud.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class BackendSirema(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        modelo = get_user_model()
        if username is None:
            username = kwargs.get(modelo.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            usuario = modelo._default_manager.get_by_natural_key(username)
        except modelo.DoesNotExist:
            modelo().set_password(password)  # mismo tiempo de respuesta que con un usuario existente
            return None
        if usuario.check_password(password):
            return usuario  # el formulario rechaza después a los desactivados con su propio mensaje
        return None
