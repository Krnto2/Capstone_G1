import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def env(nombre, defecto=None):
    return os.environ.get(nombre, defecto)


def env_bool(nombre, defecto=False):
    valor = os.environ.get(nombre)
    if valor is None:
        return defecto
    return valor.strip().lower() in {"1", "true", "si", "sí", "yes", "on"}


def env_lista(nombre, defecto=""):
    return [v.strip() for v in os.environ.get(nombre, defecto).split(",") if v.strip()]


SIREMA_VERSION = "0.9.1"

SECRET_KEY = env("DJANGO_SECRET_KEY", "solo-desarrollo-cambiar-en-produccion")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env_lista("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",
    "reportes",
    "revisiones",
    "inventario",
    "accesos",
    "nucleo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accesos.auditoria.MiddlewareAuditoria",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "nucleo.context_processors.sirema",
                "accesos.context_processors.permisos",
                "revisiones.context_processors.avisos",
            ],
        },
    },
]

if env("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER", "sirema"),
            "PASSWORD": env("POSTGRES_PASSWORD", ""),
            "HOST": env("POSTGRES_HOST", "sirema-db"),
            "PORT": env("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = "accesos.Usuario"
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "accesos.backends.BackendSirema",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [{"NAME": "accesos.validadores.RequisitosContrasena"}]

LOGIN_URL = "accesos:login"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "accesos:login"

SIREMA_SESION_DIAS = int(env("SIREMA_SESION_DIAS", "30"))
SESSION_COOKIE_AGE = SIREMA_SESION_DIAS * 24 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

AXES_ENABLED = env_bool("AXES_ENABLED", True)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_USERNAME_FORM_FIELD = "username"
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = "accesos/bloqueado.html"
AXES_VERBOSE = False
SILENCED_SYSTEM_CHECKS = ["axes.W006"]

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True
FORMAT_MODULE_PATH = ["config.formatos"]

STATIC_URL = "/static/"
STATIC_ROOT = Path(env("DJANGO_STATIC_ROOT", BASE_DIR / "staticfiles"))
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = Path(env("SIREMA_MEDIA_ROOT", BASE_DIR / "media"))

FILE_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024

SIREMA_COMPANIA = env("SIREMA_COMPANIA", "Octava Compañía")
SIREMA_DIAS_ANTICIPACION = int(env("SIREMA_DIAS_ANTICIPACION", "7"))
SIREMA_FOTO_MAX_BYTES = 10 * 1024 * 1024
SIREMA_FOTO_SALIDA_MAX_BYTES = 1024 * 1024
SIREMA_FOTO_LADO_MAXIMO = 1920
SIREMA_USAR_X_ACCEL = env_bool("SIREMA_USAR_X_ACCEL", False)
SIREMA_X_ACCEL_PREFIJO = "/protegido/"
SIREMA_RESPALDOS_DIR = Path(env("SIREMA_RESPALDOS_DIR", BASE_DIR / "respaldos"))
SIREMA_RESPALDOS_DIARIOS = 30
SIREMA_RESPALDOS_MENSUALES = 12

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "{asctime} {levelname} {name}: {message}", "style": "{"}},
    "handlers": {"consola": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["consola"], "level": "INFO"},
    "loggers": {"axes": {"level": "WARNING"}},
}
