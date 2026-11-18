from functools import wraps

from django.core.exceptions import PermissionDenied


def verificar(usuario, *codigos):
    return usuario.is_authenticated and any(usuario.tiene_permiso(c) for c in codigos)


class PermisoRequeridoMixin:
    permiso_requerido = None

    def dispatch(self, request, *args, **kwargs):
        codigos = self.permiso_requerido
        if isinstance(codigos, str):
            codigos = (codigos,)
        if codigos and not verificar(request.user, *codigos):
            raise PermissionDenied("No tiene permiso para realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)


def permiso_requerido(*codigos):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not verificar(request.user, *codigos):
                raise PermissionDenied("No tiene permiso para realizar esta acción.")
            return vista(request, *args, **kwargs)

        return envoltura

    return decorador
