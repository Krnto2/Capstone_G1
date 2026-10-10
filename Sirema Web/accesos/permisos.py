"""
Control de acceso por rol validado en el servidor (RF-02, RNF-02).

Aunque la interfaz oculte las opciones no autorizadas, cada vista vuelve a
verificar el permiso del usuario antes de ejecutar la acción.
"""
from functools import wraps

from django.core.exceptions import PermissionDenied


def verificar(usuario, *codigos):
    """True si el usuario tiene al menos uno de los permisos indicados."""
    return usuario.is_authenticated and any(usuario.tiene_permiso(c) for c in codigos)


class PermisoRequeridoMixin:
    """Mixin para vistas basadas en clases: `permiso_requerido = "codigo"` o tupla."""

    permiso_requerido = None

    def dispatch(self, request, *args, **kwargs):
        codigos = self.permiso_requerido
        if isinstance(codigos, str):
            codigos = (codigos,)
        if codigos and not verificar(request.user, *codigos):
            raise PermissionDenied("No tiene permiso para realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)


def permiso_requerido(*codigos):
    """Decorador para vistas basadas en funciones."""

    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not verificar(request.user, *codigos):
                raise PermissionDenied("No tiene permiso para realizar esta acción.")
            return vista(request, *args, **kwargs)

        return envoltura

    return decorador
