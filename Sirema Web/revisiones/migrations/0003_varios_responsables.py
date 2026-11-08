"""
Una asignación y una revisión pueden tener varios responsables.

El responsable único de cada fila pasa a las tablas nuevas, así que nadie pierde
sus revisiones. Al revertir, cada fila conserva solo a uno de sus responsables.
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

TABLAS = [("asignacion_responsable", "id_asignacion", "asignacion_plan"),
          ("revision_responsable", "id_revision", "revision")]


def copiar_responsables(apps, schema_editor):
    for destino, clave, origen in TABLAS:
        schema_editor.execute(f"INSERT INTO {destino} ({clave}, id_usuario) "
                              f"SELECT {clave}, id_usuario_responsable FROM {origen} "
                              "WHERE id_usuario_responsable IS NOT NULL")


def restaurar_responsable(apps, schema_editor):
    for destino, clave, origen in TABLAS:
        schema_editor.execute(f"UPDATE {origen} SET id_usuario_responsable = (SELECT MIN(r.id_usuario) "
                              f"FROM {destino} r WHERE r.{clave} = {origen}.{clave})")
    if schema_editor.connection.vendor == "postgresql":
        # PostgreSQL no altera una tabla con verificaciones de claves foráneas pendientes.
        schema_editor.execute("SET CONSTRAINTS ALL IMMEDIATE")


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("revisiones", "0002_fk_foto_resultado"),
    ]

    operations = [
        migrations.CreateModel(
            name="AsignacionResponsable",
            fields=[
                ("pk", models.CompositePrimaryKey("asignacion_id", "usuario_id", blank=True, editable=False,
                                                  primary_key=True, serialize=False)),
                ("asignacion", models.ForeignKey(db_column="id_asignacion", on_delete=django.db.models.deletion.CASCADE,
                                                 related_name="+", to="revisiones.asignacionplan")),
                ("usuario", models.ForeignKey(db_column="id_usuario", on_delete=django.db.models.deletion.CASCADE,
                                              related_name="+", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "asignacion_responsable"},
        ),
        migrations.CreateModel(
            name="RevisionResponsable",
            fields=[
                ("pk", models.CompositePrimaryKey("revision_id", "usuario_id", blank=True, editable=False,
                                                  primary_key=True, serialize=False)),
                ("revision", models.ForeignKey(db_column="id_revision", on_delete=django.db.models.deletion.CASCADE,
                                               related_name="+", to="revisiones.revision")),
                ("usuario", models.ForeignKey(db_column="id_usuario", on_delete=django.db.models.deletion.RESTRICT,
                                              related_name="+", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "revision_responsable"},
        ),
        # Nulo mientras dura la copia: permite revertir la migración con datos.
        migrations.AlterField(
            model_name="revision",
            name="usuario_responsable",
            field=models.ForeignKey(db_column="id_usuario_responsable", null=True,
                                    on_delete=django.db.models.deletion.RESTRICT,
                                    related_name="revisiones_responsable", to=settings.AUTH_USER_MODEL,
                                    verbose_name="responsable"),
        ),
        migrations.RunPython(copiar_responsables, restaurar_responsable),
        migrations.RemoveIndex(model_name="revision", name="ix_revision_responsable"),
        migrations.RemoveField(model_name="asignacionplan", name="usuario_responsable"),
        migrations.RemoveField(model_name="revision", name="usuario_responsable"),
        migrations.AddField(
            model_name="asignacionplan",
            name="responsables",
            field=models.ManyToManyField(related_name="asignaciones_responsable",
                                         through="revisiones.AsignacionResponsable", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="revision",
            name="responsables",
            field=models.ManyToManyField(related_name="revisiones_responsable",
                                         through="revisiones.RevisionResponsable", to=settings.AUTH_USER_MODEL),
        ),
    ]
