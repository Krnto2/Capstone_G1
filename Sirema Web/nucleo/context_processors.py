from django.conf import settings


def sirema(request):
    return {
        "SIREMA_VERSION": settings.SIREMA_VERSION,
        "SIREMA_COMPANIA": settings.SIREMA_COMPANIA,
    }
