"""Perfil del usuario: datos propios, foto y reglas de contraseña."""
import io

import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from accesos.models import EventoAuditoria, FotoPerfil, Rol

pytestmark = pytest.mark.django_db


def _datos(usuario, **cambios):
    return {"nombre": usuario.nombre, "apellidos": usuario.apellidos, "correo": usuario.correo,
            "telefono": usuario.telefono or "", **cambios}


class TestDatosDelPerfil:
    def test_el_titular_corrige_sus_datos(self, client, bombero):
        client.force_login(bombero)
        respuesta = client.post(reverse("accesos:perfil_editar"), _datos(
            bombero, nombre="Juan Pablo", correo="NUEVO@prueba.cl", telefono="+56 9 1234 5678"))
        assert respuesta.status_code == 302
        bombero.refresh_from_db()
        assert (bombero.nombre, bombero.correo, bombero.telefono) == ("Juan Pablo", "nuevo@prueba.cl",
                                                                      "+56 9 1234 5678")
        evento = EventoAuditoria.objects.filter(usuario=bombero, entidad_afectada="usuario").latest("id")
        assert evento.datos_nuevos["nombre"] == "Juan Pablo" and evento.datos_anteriores["nombre"] == "Juan"

    def test_no_permite_cambiar_rut_ni_rol(self, client, bombero):
        client.force_login(bombero)
        rut = bombero.rut
        client.post(reverse("accesos:perfil_editar"), _datos(
            bombero, rut="11.111.111-1", rol=Rol.objects.get(nombre=Rol.ADMINISTRADOR).pk))
        bombero.refresh_from_db()
        assert bombero.rut == rut and bombero.rol.nombre == Rol.BOMBERO

    def test_rechaza_correo_de_otro_usuario(self, client, bombero, otro_bombero):
        client.force_login(bombero)
        respuesta = client.post(reverse("accesos:perfil_editar"), _datos(bombero, correo=otro_bombero.correo.upper()))
        assert "ya existe" in str(respuesta.context["form"].errors["correo"]).lower()

    @pytest.mark.parametrize("telefono", ["renatopomeri8@g", "12345", "+56 abc 1234"])
    def test_rechaza_telefonos_invalidos(self, client, bombero, telefono):
        client.force_login(bombero)
        respuesta = client.post(reverse("accesos:perfil_editar"), _datos(bombero, telefono=telefono))
        assert "telefono" in respuesta.context["form"].errors

    def test_un_error_no_cambia_el_nombre_que_se_muestra(self, client, bombero):
        client.force_login(bombero)
        respuesta = client.post(reverse("accesos:perfil_editar"), _datos(bombero, nombre="Otro", correo="malo"))
        assert respuesta.status_code == 200
        assert respuesta.context["user"].nombre == "Juan"

    def test_el_telefono_es_opcional(self, client, bombero):
        client.force_login(bombero)
        assert client.post(reverse("accesos:perfil_editar"), _datos(bombero, telefono="")).status_code == 302
        bombero.refresh_from_db()
        assert bombero.telefono is None


class TestFotoDePerfil:
    def _subir(self, client, usuario, archivo):
        client.force_login(usuario)
        return client.post(reverse("accesos:foto_perfil_subir"), {"foto": archivo}, follow=True)

    def _foto(self, client, usuario):
        return client.get(reverse("accesos:foto_perfil", args=[usuario.pk]))

    def test_se_guarda_y_se_ve(self, client, bombero, imagen):
        self._subir(client, bombero, imagen())
        bombero.refresh_from_db()
        assert bombero.tiene_foto
        respuesta = self._foto(client, bombero)
        assert respuesta.status_code == 200 and respuesta["Content-Type"] == "image/jpeg"
        assert Image.open(io.BytesIO(respuesta.content)).format == "JPEG"

    def test_se_ve_en_produccion_aunque_no_exista_nginx_ni_media(self, client, bombero, imagen, settings, tmp_path):
        settings.SIREMA_USAR_X_ACCEL = True
        settings.MEDIA_ROOT = tmp_path / "no-existe"
        self._subir(client, bombero, imagen())
        respuesta = self._foto(client, bombero)
        assert len(respuesta.content) > 0 and "X-Accel-Redirect" not in respuesta.headers
        assert not settings.MEDIA_ROOT.exists()

    def test_queda_cuadrada_y_liviana(self, client, bombero, imagen):
        self._subir(client, bombero, imagen(tamano=(1600, 900), formato="PNG", nombre="foto.png"))
        foto = Image.open(io.BytesIO(bytes(FotoPerfil.objects.get(pk=bombero.pk).imagen)))
        assert foto.size == (320, 320)

    def test_reemplazar_cambia_la_version_para_refrescar_el_navegador(self, client, bombero, imagen):
        self._subir(client, bombero, imagen())
        bombero.refresh_from_db()
        anterior = bombero.foto_version
        self._subir(client, bombero, imagen(color=(200, 30, 30)))
        bombero.refresh_from_db()
        assert bombero.foto_version != anterior and FotoPerfil.objects.count() == 1

    def test_quitar_vuelve_a_las_iniciales(self, client, bombero, imagen):
        self._subir(client, bombero, imagen())
        client.post(reverse("accesos:foto_perfil_eliminar"))
        bombero.refresh_from_db()
        assert not bombero.tiene_foto and not FotoPerfil.objects.exists()
        assert self._foto(client, bombero).status_code == 404

    def test_rechaza_lo_que_no_es_imagen(self, client, bombero):
        respuesta = self._subir(client, bombero, SimpleUploadedFile("foto.jpg", b"no soy una imagen"))
        assert "imagen válida" in str(list(respuesta.context["messages"])[0])
        bombero.refresh_from_db()
        assert not bombero.tiene_foto

    def test_otro_bombero_no_ve_la_foto(self, client, bombero, otro_bombero, imagen):
        self._subir(client, bombero, imagen())
        client.force_login(otro_bombero)
        assert self._foto(client, bombero).status_code == 403

    def test_el_administrador_si(self, client, bombero, administrador, imagen):
        self._subir(client, bombero, imagen())
        client.force_login(administrador)
        assert self._foto(client, bombero).status_code == 200


class TestContrasena:
    @pytest.mark.parametrize("clave", ["Ab1!", "Clave2026#", "Ñandú 8", "Z9_"])
    def test_acepta_mayuscula_numero_y_caracter_especial(self, clave):
        validate_password(clave)

    @pytest.mark.parametrize("clave", ["sinmayuscula1!", "SinNumero!", "SinEspecial1", ""])
    def test_rechaza_si_falta_alguno(self, clave):
        with pytest.raises(ValidationError, match="mayúscula"):
            validate_password(clave)

    def test_no_compara_con_los_datos_del_usuario(self, bombero):
        validate_password("Juan1!", bombero)
