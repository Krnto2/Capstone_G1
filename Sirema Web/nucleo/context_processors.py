from django.conf import settings


def sirema(request):
    return {
        "SIREMA_VERSION": settings.SIREMA_VERSION,
        "SIREMA_COMPANIA": settings.SIREMA_COMPANIA,
        "SIREMA_SESION_MINUTOS": settings.SESSION_COOKIE_AGE // 60,
    }
