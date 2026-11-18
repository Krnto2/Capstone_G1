from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("accesos", "0005_usuario_sesion_activa")]

    operations = [
        migrations.RemoveField(model_name="usuario", name="sesion_activa"),
    ]
