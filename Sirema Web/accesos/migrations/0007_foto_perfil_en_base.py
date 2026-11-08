"""
La foto de perfil pasa del volumen media a la base de datos.

Las fotos cuyo archivo ya no existe no se pueden recuperar: esos usuarios vuelven a
mostrar sus iniciales hasta que suban una nueva.
"""
import hashlib
import io

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from nucleo.almacenamiento import ErrorAlmacenamiento, ServicioAlmacenamiento, foto_de_perfil


def mover_fotos(apps, schema_editor):
    Usuario = apps.get_model("accesos", "Usuario")
    FotoPerfil = apps.get_model("accesos", "FotoPerfil")
    almacen = ServicioAlmacenamiento()
    for usuario in Usuario.objects.exclude(foto_perfil__isnull=True).exclude(foto_perfil=""):
        try:
            imagen = foto_de_perfil(io.BytesIO(almacen.leer(usuario.foto_perfil)))
        except (OSError, ErrorAlmacenamiento):
            continue
        FotoPerfil.objects.create(usuario=usuario, imagen=imagen)
        usuario.foto_version = hashlib.sha256(imagen).hexdigest()[:16]
        usuario.save(update_fields=["foto_version"])


class Migration(migrations.Migration):
    dependencies = [("accesos", "0006_quitar_sesion_activa")]

    operations = [
        migrations.CreateModel(
            name="FotoPerfil",
            fields=[
                ("usuario", models.OneToOneField(db_column="id_usuario", on_delete=django.db.models.deletion.CASCADE,
                                                 primary_key=True, related_name="foto", serialize=False,
                                                 to=settings.AUTH_USER_MODEL)),
                ("imagen", models.BinaryField()),
            ],
            options={"db_table": "foto_perfil"},
        ),
        migrations.AddField(
            model_name="usuario",
            name="foto_version",
            field=models.CharField(blank=True, editable=False, max_length=16, null=True),
        ),
        migrations.RunPython(mover_fotos, migrations.RunPython.noop),
        migrations.RemoveField(model_name="usuario", name="foto_perfil"),
    ]
