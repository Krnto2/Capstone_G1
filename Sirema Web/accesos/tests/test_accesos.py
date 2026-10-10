"""CP-01 Gestión de usuarios y CP-02 Autenticación y control de acceso por rol."""
import pytest
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.urls import reverse

from accesos import auditoria
from accesos.forms import FormularioUsuario
from accesos.models import EventoAuditoria, Rol, RolPermiso, Usuario
from conftest import CLAVE

pytestmark = pytest.mark.django_db


class TestCP01Usuarios:
    def _datos(self, **extra):
        datos = {"rut": "18.888.888-7", "nombre": "Luis", "apellidos": "Prueba", "correo": "luis@prueba.cl",
                 "telefono": "", "rol": Rol.objects.get(nombre=Rol.BOMBERO).pk,
                 "contrasena1": "Clave1234x", "contrasena2": "Clave1234x"}
        datos.update(extra)
        return datos

    def test_crea_usuario_con_contrasena_argon2(self):
        form = FormularioUsuario(self._datos())
        assert form.is_valid(), form.errors
        usuario = form.save()
        assert usuario.password.startswith("argon2")
        assert usuario.check_password("Clave1234x")

    def test_no_admite_rut_ni_correo_repetidos(self, bombero):
        form = FormularioUsuario(self._datos(rut=bombero.rut, correo=bombero.correo.upper()))
        assert not form.is_valid()
        assert "rut" in form.errors and "correo" in form.errors

    def test_rut_con_digito_verificador_incorrecto(self):
        form = FormularioUsuario(self._datos(rut="18.888.888-0"))
        assert not form.is_valid() and "rut" in form.errors

    def test_contrasena_debe_ser_alfanumerica_y_de_8_caracteres(self):
        assert "contrasena1" in FormularioUsuario(self._datos(contrasena1="abcdefgh", contrasena2="abcdefgh")).errors
        assert "contrasena1" in FormularioUsuario(self._datos(contrasena1="Ab1", contrasena2="Ab1")).errors

    def test_no_se_desactiva_ni_degrada_al_unico_administrador(self, administrador):
        with pytest.raises(ValidationError):
            administrador.desactivar()
        form = FormularioUsuario({**self._datos(rut=administrador.rut, correo=administrador.correo),
                                  "rol": Rol.objects.get(nombre=Rol.BOMBERO).pk}, instance=administrador)
        assert "rol" in form.errors

    def test_usuario_desactivado_no_ingresa_y_conserva_historial(self, client, bombero):
        bombero.desactivar()
        assert Usuario.objects.filter(pk=bombero.pk).exists()
        respuesta = client.post(reverse("accesos:login"), {"username": bombero.correo, "password": CLAVE})
        assert respuesta.status_code == 200 and not respuesta.wsgi_request.user.is_authenticated


class TestCP02ControlDeAcceso:
    def test_ninguna_pagina_sin_sesion_salvo_el_ingreso(self, client):
        assert client.get(reverse("accesos:login")).status_code == 200
        for nombre in ["inicio", "inventario:lista", "revisiones:mis_revisiones", "reportes:panel",
                       "accesos:usuarios"]:
            respuesta = client.get(reverse(nombre))
            assert respuesta.status_code == 302 and reverse("accesos:login") in respuesta.url

    def test_ingreso_con_correo_sin_distinguir_mayusculas(self, client, bombero):
        respuesta = client.post(reverse("accesos:login"), {"username": "BOMBERO@prueba.cl", "password": CLAVE})
        assert respuesta.status_code == 302
        assert EventoAuditoria.objects.filter(usuario=bombero, accion="acceso").exists()

    @pytest.mark.parametrize("nombre", ["reportes:panel", "accesos:usuarios", "accesos:bitacora",
                                        "revisiones:planes", "inventario:crear", "inventario:unidades"])
    def test_bombero_sin_accesos_indebidos(self, client, bombero, nombre):
        client.force_login(bombero)
        assert client.get(reverse(nombre)).status_code == 403

    @pytest.mark.parametrize("nombre", ["accesos:usuarios", "accesos:bitacora", "inventario:unidades"])
    def test_jefatura_sin_funciones_de_administracion(self, client, jefatura, nombre):
        client.force_login(jefatura)
        assert client.get(reverse(nombre)).status_code == 403

    def test_cada_rol_llega_a_su_inicio(self, client, bombero, jefatura, administrador):
        for usuario, destino in [(bombero, "revisiones:mis_revisiones"), (jefatura, "reportes:panel"),
                                 (administrador, "revisiones:mis_revisiones")]:
            client.force_login(usuario)
            assert client.get(reverse("inicio")).url == reverse(destino)

    def test_cambio_de_contrasena_exige_la_actual(self, client, bombero):
        client.force_login(bombero)
        url = reverse("accesos:cambiar_contrasena")
        mala = client.post(url, {"old_password": "otra", "new_password1": "Nueva2026x", "new_password2": "Nueva2026x"})
        assert mala.status_code == 200
        buena = client.post(url, {"old_password": CLAVE, "new_password1": "Nueva2026x", "new_password2": "Nueva2026x"})
        assert buena.status_code == 302
        bombero.refresh_from_db()
        assert bombero.check_password("Nueva2026x")

    def test_matriz_de_permisos_protege_al_administrador(self, client, administrador):
        client.force_login(administrador)
        client.post(reverse("accesos:permisos"), {})  # desmarca todo
        admin = Rol.objects.get(nombre=Rol.ADMINISTRADOR)
        codigos = set(RolPermiso.objects.filter(rol=admin).values_list("permiso__codigo", flat=True))
        assert codigos == {"usuario.administrar", "permiso.administrar"}
        assert EventoAuditoria.objects.filter(entidad_afectada="rol_permiso").exists()


class TestBitacora:
    def test_registra_con_usuario_sistema_sin_request(self):
        evento = auditoria.registrar("alta", "prueba", 1, nuevos={"x": 1})
        assert evento.usuario.correo == "sistema@sirema.local"

    def test_la_bitacora_es_inmutable(self, bombero):
        evento = auditoria.registrar("alta", "prueba", 1, usuario=bombero)
        with pytest.raises(ValidationError):
            evento.save()
        with pytest.raises(ValidationError):
            evento.delete()
        with pytest.raises(Exception), transaction.atomic(), connection.cursor() as cursor:
            cursor.execute("DELETE FROM evento_auditoria WHERE id_evento = %s", [evento.pk])


class TestUsuariosDemo:
    def _crear_demo(self):
        from accesos.demo import USUARIOS_DEMO
        cuerpo, nombre, apellidos, correo, rol = USUARIOS_DEMO[1]
        Usuario.objects.create(rut="12.345.678-5", nombre=nombre, apellidos=apellidos, correo=correo,
                               rol=Rol.objects.get(nombre=rol), password="!")

    def test_se_muestran_en_el_ingreso_solo_con_debug(self, client, settings):
        self._crear_demo()
        settings.DEBUG = True
        assert len(client.get(reverse("accesos:login")).context["usuarios_demo"]) == 1
        settings.DEBUG = False
        respuesta = client.get(reverse("accesos:login"))
        assert respuesta.context["usuarios_demo"] == [] and respuesta.context["contrasena_demo"] is None
