from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accesos", "0003_bitacora_inmutable"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="foto_perfil",
            field=models.CharField(blank=True, db_column="foto_perfil", max_length=300,
                                   null=True, verbose_name="foto de perfil"),
        ),
    ]
