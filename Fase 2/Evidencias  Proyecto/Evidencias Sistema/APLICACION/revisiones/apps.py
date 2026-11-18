from django.apps import AppConfig


class RevisionesConfig(AppConfig):
    name = "revisiones"
    verbose_name = "Revisiones periódicas"

    def ready(self):
        from inventario import registro

        from .signals import ProveedorFichaMaterial

        registro.registrar_proveedor(ProveedorFichaMaterial())
