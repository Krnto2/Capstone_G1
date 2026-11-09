"""RNF-05: respaldos manuales, descarga y restauración completa desde la pantalla del administrador."""
import io
import json
import zipfile
from pathlib import Path

import pytest
from django.contrib.sessions.models import Session
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import Client
from django.urls import reverse

from accesos.models import EventoAuditoria, Usuario
from conftest import CLAVE
from inventario.models import Categoria
from nucleo import respaldos

TRIGGERS_SQLITE = [
    """CREATE TRIGGER IF NOT EXISTS tg_evento_auditoria_sin_update BEFORE UPDATE ON evento_auditoria
       BEGIN SELECT RAISE(ABORT, 'La bitacora de auditoria no se puede modificar'); END;""",
    """CREATE TRIGGER IF NOT EXISTS tg_evento_auditoria_sin_delete BEFORE DELETE ON evento_auditoria
       BEGIN SELECT RAISE(ABORT, 'La bitacora de auditoria no se puede eliminar'); END;""",
]


@pytest.fixture
def cliente_admin(administrador):
    cliente = Client()
    cliente.force_login(administrador)
    return cliente


@pytest.fixture
def bitacora_limpiable():
    """Las pruebas con transacciones reales dejan filas en la bitácora inmutable: se limpian al final."""
    yield
    if connection.vendor != "sqlite":
        return
    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS tg_evento_auditoria_sin_update")
        cursor.execute("DROP TRIGGER IF EXISTS tg_evento_auditoria_sin_delete")
        cursor.execute("DELETE FROM evento_auditoria")
        for sql in TRIGGERS_SQLITE:
            cursor.execute(sql)


def _zip(contenido):
    bufer = io.BytesIO()
    with zipfile.ZipFile(bufer, "w") as zf:
        for nombre, datos in contenido.items():
            zf.writestr(nombre, datos)
    return SimpleUploadedFile("sirema_20260101_000000.zip", bufer.getvalue(), content_type="application/zip")


@pytest.mark.django_db
class TestGenerarYDescargar:
    def test_solo_el_administrador_ve_la_pantalla(self, client, jefatura, bombero, cliente_admin):
        for usuario in (jefatura, bombero):
            client.force_login(usuario)
            assert client.get(reverse("accesos:respaldos")).status_code == 403
            assert client.post(reverse("accesos:respaldo_crear")).status_code == 403
        assert cliente_admin.get(reverse("accesos:respaldos")).status_code == 200

    def test_genera_un_zip_completo_con_fotos(self, cliente_admin, settings):
        foto = Path(settings.MEDIA_ROOT) / "evidencias" / "a.jpg"
        foto.parent.mkdir(parents=True)
        foto.write_bytes(b"jpeg")
        respuesta = cliente_admin.post(reverse("accesos:respaldo_crear"))
        assert respuesta.status_code == 302
        [r] = respaldos.listar()
        assert r.tipo == "Manual"
        with zipfile.ZipFile(r.ruta) as zf:
            nombres = zf.namelist()
            manifiesto = json.loads(zf.read("manifiesto.json"))
        assert "base/db.sqlite3" in nombres and "media/evidencias/a.jpg" in nombres
        assert manifiesto["motor"] == "sqlite" and ["accesos", "0008_permiso_respaldos"] in manifiesto["migraciones"]
        assert EventoAuditoria.objects.filter(entidad_afectada="respaldo", accion="alta").exists()

    def test_descarga_y_elimina(self, cliente_admin):
        ruta = respaldos.crear_respaldo("manuales")
        url = reverse("accesos:respaldo_descargar", args=["manuales", ruta.name])
        respuesta = cliente_admin.get(url)
        assert respuesta.status_code == 200
        assert respuesta["Content-Type"] == "application/zip"
        assert zipfile.ZipFile(io.BytesIO(b"".join(respuesta.streaming_content))).testzip() is None
        cliente_admin.post(reverse("accesos:respaldo_eliminar", args=["manuales", ruta.name]))
        assert not ruta.exists()

    @pytest.mark.parametrize("carpeta,nombre", [("manuales", "..%2F..%2Fdb.sqlite3"), ("otra", "sirema_20260101_000000.zip"),
                                                ("manuales", "sirema_20260101_000000.zip")])
    def test_no_entrega_rutas_arbitrarias(self, cliente_admin, carpeta, nombre):
        respuesta = cliente_admin.get(f"/accesos/respaldos/{carpeta}/{nombre}/descargar/")
        assert respuesta.status_code == 404

    def test_el_respaldo_diario_usa_el_mismo_formato_y_rota(self, settings, administrador):
        from django.core.management import call_command

        settings.SIREMA_RESPALDOS_DIARIOS = 2
        for _ in range(3):
            call_command("respaldo_diario", stdout=io.StringIO())
        diarios = [r for r in respaldos.listar() if r.tipo == "Diario"]
        assert 1 <= len(diarios) <= 2


@pytest.mark.django_db
class TestValidacionRestauracion:
    def _restaurar(self, cliente, archivo, contrasena=CLAVE, confirmacion="RESTAURAR"):
        return cliente.post(reverse("accesos:respaldo_restaurar"),
                            {"archivo": archivo, "contrasena": contrasena, "confirmacion": confirmacion})

    def test_exige_contrasena_y_confirmacion(self, cliente_admin):
        archivo = _zip({"x": "y"})
        respuesta = self._restaurar(cliente_admin, archivo, contrasena="mala", confirmacion="si")
        assert respuesta.status_code == 400
        errores = respuesta.context["form"].errors
        assert "contrasena" in errores and "confirmacion" in errores

    @pytest.mark.parametrize("contenido,mensaje", [
        ({"hola.txt": "x"}, "falta el manifiesto"),
        ({"manifiesto.json": json.dumps({"aplicacion": "SIREMA", "formato": 1, "motor": "postgresql"})}, "postgresql"),
        ({"manifiesto.json": json.dumps({"aplicacion": "SIREMA", "formato": 1, "motor": "sqlite"})}, "no contiene"),
        ({"manifiesto.json": json.dumps({"aplicacion": "SIREMA", "formato": 1, "motor": "sqlite",
                                         "migraciones": [["accesos", "9999_futura"]]}),
          "base/db.sqlite3": "x"}, "más nueva"),
        ({"manifiesto.json": "{}", "../fuera.txt": "x"}, "rutas no permitidas"),
    ])
    def test_rechaza_archivos_invalidos_sin_tocar_datos(self, cliente_admin, contenido, mensaje):
        usuarios = Usuario.objects.count()
        respuesta = self._restaurar(cliente_admin, _zip(contenido))
        assert respuesta.status_code == 400
        assert mensaje in " ".join(respuesta.context["form"].non_field_errors())
        assert Usuario.objects.count() == usuarios
        assert respaldos.listar() == []  # no se generó la copia previa

    def test_rechaza_un_archivo_que_no_es_zip(self, cliente_admin):
        archivo = SimpleUploadedFile("respaldo.zip", b"no soy un zip")
        respuesta = self._restaurar(cliente_admin, archivo)
        assert "no es un .zip" in " ".join(respuesta.context["form"].non_field_errors())


@pytest.mark.django_db(transaction=True, serialized_rollback=True)
class TestRestauracionCompleta:
    def test_restaura_datos_y_fotos_y_cierra_sesiones(self, bitacora_limpiable, administrador, settings):
        media = Path(settings.MEDIA_ROOT)
        (media / "evidencias").mkdir(parents=True)
        (media / "evidencias" / "original.jpg").write_bytes(b"original")
        Categoria.objects.create(nombre="Antes del respaldo")
        cliente = Client()
        cliente.force_login(administrador)
        cliente.post(reverse("accesos:respaldo_crear"))
        [respaldo] = respaldos.listar()
        descargado = b"".join(cliente.get(reverse("accesos:respaldo_descargar",
                                                  args=["manuales", respaldo.nombre])).streaming_content)

        # Cambios posteriores que la restauración debe deshacer.
        Categoria.objects.create(nombre="Después del respaldo")
        (media / "evidencias" / "nueva.jpg").write_bytes(b"nueva")
        (media / "evidencias" / "original.jpg").unlink()

        respuesta = cliente.post(reverse("accesos:respaldo_restaurar"), {
            "archivo": SimpleUploadedFile(respaldo.nombre, descargado, content_type="application/zip"),
            "contrasena": CLAVE, "confirmacion": "RESTAURAR"})

        assert respuesta.status_code == 302 and respuesta.url == reverse("accesos:login")
        nombres = set(Categoria.objects.values_list("nombre", flat=True))
        assert "Antes del respaldo" in nombres and "Después del respaldo" not in nombres
        assert (media / "evidencias" / "original.jpg").read_bytes() == b"original"
        assert not (media / "evidencias" / "nueva.jpg").exists()
        assert not Session.objects.exists()
        assert cliente.get(reverse("accesos:respaldos")).status_code == 302  # debe ingresar de nuevo
        assert any("antes_de_restaurar" in r.nombre for r in respaldos.listar())
        assert EventoAuditoria.objects.filter(entidad_afectada="respaldo", accion="modificacion").exists()

    def test_restaura_un_respaldo_guardado_en_el_servidor(self, bitacora_limpiable, administrador):
        ruta = respaldos.crear_respaldo("diarios")
        Categoria.objects.create(nombre="Temporal")
        cliente = Client()
        cliente.force_login(administrador)
        respuesta = cliente.post(reverse("accesos:respaldo_restaurar"), {
            "origen": f"diarios/{ruta.name}", "contrasena": CLAVE, "confirmacion": "RESTAURAR"})
        assert respuesta.status_code == 302
        assert not Categoria.objects.filter(nombre="Temporal").exists()
