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
            modelo().set_password(password)
            return None
        if usuario.check_password(password):
            return usuario
        return None
