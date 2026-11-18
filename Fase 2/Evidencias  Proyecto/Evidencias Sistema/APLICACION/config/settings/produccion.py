from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import DATABASES, SECRET_KEY, SILENCED_SYSTEM_CHECKS, env_lista

DEBUG = False

if SECRET_KEY.startswith("solo-desarrollo"):
    raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY en el archivo .env.")
if DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":
    raise ImproperlyConfigured("En producción SIREMA usa PostgreSQL: defina POSTGRES_DB.")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
CSRF_TRUSTED_ORIGINS = env_lista("DJANGO_CSRF_TRUSTED_ORIGINS", "https://sirema.local")

SIREMA_USAR_X_ACCEL = True

SILENCED_SYSTEM_CHECKS = [*SILENCED_SYSTEM_CHECKS, "security.W004", "security.W008"]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
