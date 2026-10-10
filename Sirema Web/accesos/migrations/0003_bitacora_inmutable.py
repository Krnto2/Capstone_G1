"""RNF-09: un disparador rechaza cualquier UPDATE o DELETE sobre evento_auditoria."""
from django.db import migrations

POSTGRES = [
    """
    CREATE OR REPLACE FUNCTION evento_auditoria_inmutable() RETURNS trigger AS $$
    BEGIN
        RAISE EXCEPTION 'La bitácora de auditoría no se puede modificar ni eliminar';
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER tg_evento_auditoria_inmutable
    BEFORE UPDATE OR DELETE ON evento_auditoria
    FOR EACH ROW EXECUTE FUNCTION evento_auditoria_inmutable();
    """,
]
POSTGRES_REVERSA = [
    "DROP TRIGGER IF EXISTS tg_evento_auditoria_inmutable ON evento_auditoria;",
    "DROP FUNCTION IF EXISTS evento_auditoria_inmutable();",
]
SQLITE = [
    """CREATE TRIGGER IF NOT EXISTS tg_evento_auditoria_sin_update BEFORE UPDATE ON evento_auditoria
       BEGIN SELECT RAISE(ABORT, 'La bitacora de auditoria no se puede modificar'); END;""",
    """CREATE TRIGGER IF NOT EXISTS tg_evento_auditoria_sin_delete BEFORE DELETE ON evento_auditoria
       BEGIN SELECT RAISE(ABORT, 'La bitacora de auditoria no se puede eliminar'); END;""",
]
SQLITE_REVERSA = [
    "DROP TRIGGER IF EXISTS tg_evento_auditoria_sin_update;",
    "DROP TRIGGER IF EXISTS tg_evento_auditoria_sin_delete;",
]


def _ejecutar(schema_editor, sentencias):
    for sql in sentencias:
        schema_editor.execute(sql)


def crear(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        _ejecutar(schema_editor, POSTGRES)
    elif vendor == "sqlite":
        _ejecutar(schema_editor, SQLITE)


def eliminar(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        _ejecutar(schema_editor, POSTGRES_REVERSA)
    elif vendor == "sqlite":
        _ejecutar(schema_editor, SQLITE_REVERSA)


class Migration(migrations.Migration):
    dependencies = [("accesos", "0002_datos_iniciales")]
    operations = [migrations.RunPython(crear, eliminar)]
