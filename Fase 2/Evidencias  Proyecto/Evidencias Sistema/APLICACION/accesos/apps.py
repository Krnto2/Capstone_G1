from django.apps import AppConfig


class AccesosConfig(AppConfig):
    name = "accesos"
    verbose_name = "Usuarios y accesos"

    def ready(self):
        from . import signals  # noqa: F401
