from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accesos", "0004_usuario_foto_perfil"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="sesion_activa",
            field=models.CharField(blank=True, db_column="sesion_activa", max_length=40,
                                   null=True, verbose_name="sesión activa"),
        ),
    ]
