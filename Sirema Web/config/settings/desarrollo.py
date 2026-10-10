"""Configuración para el equipo de desarrollo (SQLite si no hay PostgreSQL)."""
from .base import *  # noqa: F401,F403
from .base import env_bool

DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = ["*"]
