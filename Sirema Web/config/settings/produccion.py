"""Configuración del servidor del cuartel (Docker Compose detrás de Nginx)."""
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import DATABASES, SECRET_KEY, SILENCED_SYSTEM_CHECKS, env_lista

DEBUG = False

if SECRET_KEY.startswith("solo-desarrollo"):
    raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY en el archivo .env.")
if DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":
    raise ImproperlyConfigured("En producción SIREMA usa PostgreSQL: defina POSTGRES_DB.")

# Nginx termina TLS (HTTPS) y reenvía por HTTP interno.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
CSRF_TRUSTED_ORIGINS = env_lista("DJANGO_CSRF_TRUSTED_ORIGINS", "https://sirema.local")

SIREMA_USAR_X_ACCEL = True

# Nginx redirige el puerto 80 a HTTPS (si Django también lo hiciera, se romperían los
# healthchecks internos), y no se activa HSTS porque el certificado es autofirmado y de red local.
SILENCED_SYSTEM_CHECKS = [*SILENCED_SYSTEM_CHECKS, "security.W004", "security.W008"]

# Nombres de archivo con hash: los celulares nunca usan una versión vieja del CSS o JS.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
