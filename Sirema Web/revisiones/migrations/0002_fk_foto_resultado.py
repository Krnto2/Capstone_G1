"""
fk_foto_resultado: clave foránea compuesta fotografia(id_revision, id_punto) ->
resultado_punto(id_revision, id_punto). El ORM de Django 5.2 no admite claves
foráneas compuestas, por lo que se crea con SQL explícito (DAS 4.2.5). Si
id_punto es nulo, la fotografía es general de la revisión y no se verifica.
"""
from django.db import migrations


def crear(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            "ALTER TABLE fotografia ADD CONSTRAINT fk_foto_resultado "
            "FOREIGN KEY (id_revision, id_punto) REFERENCES resultado_punto (id_revision, id_punto) "
            "ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;"
        )


def eliminar(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("ALTER TABLE fotografia DROP CONSTRAINT IF EXISTS fk_foto_resultado;")


class Migration(migrations.Migration):
    dependencies = [("revisiones", "0001_initial")]
    operations = [migrations.RunPython(crear, eliminar)]
