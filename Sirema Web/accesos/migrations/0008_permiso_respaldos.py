"""Permiso para generar, descargar y restaurar respaldos completos (solo administrador)."""
from django.db import migrations

CODIGO = "respaldo.administrar"


def agregar(apps, schema_editor):
    Permiso = apps.get_model("accesos", "Permiso")
    Rol = apps.get_model("accesos", "Rol")
    RolPermiso = apps.get_model("accesos", "RolPermiso")
    permiso, _ = Permiso.objects.get_or_create(
        codigo=CODIGO, defaults={"nombre": "Generar, descargar y restaurar respaldos", "modulo": "accesos"})
    rol = Rol.objects.filter(nombre="administrador").first()
    if rol and not RolPermiso.objects.filter(rol=rol, permiso=permiso).exists():
        RolPermiso.objects.create(rol=rol, permiso=permiso)


def quitar(apps, schema_editor):
    apps.get_model("accesos", "Permiso").objects.filter(codigo=CODIGO).delete()


class Migration(migrations.Migration):
    dependencies = [("accesos", "0007_foto_perfil_en_base")]
    operations = [migrations.RunPython(agregar, quitar)]
