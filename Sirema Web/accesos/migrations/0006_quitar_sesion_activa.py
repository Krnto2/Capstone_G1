from django.db import migrations


class Migration(migrations.Migration):
    """Un usuario puede tener varias sesiones abiertas a la vez: ya no se guarda cuál es la activa."""

    dependencies = [("accesos", "0005_usuario_sesion_activa")]

    operations = [
        migrations.RemoveField(model_name="usuario", name="sesion_activa"),
    ]
