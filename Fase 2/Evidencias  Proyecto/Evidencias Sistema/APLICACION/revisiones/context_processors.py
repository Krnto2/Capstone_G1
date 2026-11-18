from nucleo.enums import EstadoHallazgo

from .models import Hallazgo, Notificacion


def avisos(request):
    usuario = getattr(request, "user", None)
    if usuario is None or not usuario.is_authenticated:
        return {}
    contexto = {"notificaciones_no_leidas": Notificacion.objects.filter(usuario=usuario, leida=False).count()}
    if usuario.tiene_permiso("hallazgo.gestionar"):
        contexto["hallazgos_abiertos"] = Hallazgo.objects.exclude(estado=EstadoHallazgo.CERRADO).count()
    return contexto
