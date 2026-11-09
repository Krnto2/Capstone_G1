"""CP-03 a CP-06: material, código único, búsqueda y movimientos."""
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accesos.models import EventoAuditoria
from inventario import importacion, services
from inventario.models import Material, Movimiento
from nucleo.enums import EstadoRevision

pytestmark = pytest.mark.django_db


class TestCP03Material:
    def test_registro_crea_movimiento_inicial_y_bitacora(self, material):
        assert material.activo
        inicial = Movimiento.objects.get(material=material)
        assert inicial.cajonera_origen is None and inicial.cajonera_destino == material.cajonera
        assert EventoAuditoria.objects.filter(entidad_afectada="material", accion="alta",
                                              id_registro=str(material.pk)).exists()

    def test_unitario_exige_codigo(self, catalogo, jefatura):
        with pytest.raises(ValidationError):
            services.registrar_material({"nombre": "Sin código", "categoria": catalogo["motores"],
                                         "cajonera": catalogo["cabina"], "tipo": "unitario"}, jefatura)

    def test_granel_sin_codigo_y_con_cantidad(self, catalogo, jefatura):
        guantes = services.registrar_material({"nombre": "Guantes", "categoria": catalogo["motores"],
                                               "cajonera": catalogo["cabina"], "tipo": "granel", "cantidad": 12},
                                              jefatura)
        assert guantes.codigo_institucional is None and guantes.cantidad == 12

    def test_modificar_registra_valores_anterior_y_nuevo(self, material, jefatura):
        services.modificar_material(material, {"codigo_institucional": "8C-0112", "nombre": "Motobomba Honda",
                                               "categoria": material.categoria, "tipo": "unitario"}, jefatura)
        evento = EventoAuditoria.objects.filter(accion="modificacion", entidad_afectada="material").first()
        assert evento.datos_anteriores["nombre"] == "Motobomba portátil"
        assert evento.datos_nuevos["nombre"] == "Motobomba Honda"

    def test_baja_logica_cierra_asignaciones_y_revisiones(self, revision, jefatura):
        material = revision.material
        material.dar_de_baja("Roto en emergencia", jefatura)
        revision.refresh_from_db()
        revision.asignacion.refresh_from_db()
        assert material.estado == "de_baja" and material.baja.motivo == "Roto en emergencia"
        assert not revision.asignacion.activa
        assert revision.estado == EstadoRevision.NO_REALIZADA
        with pytest.raises(ValidationError):
            material.dar_de_baja("otra vez", jefatura)

    def test_carga_masiva_registra_validas_e_informa_rechazadas(self, catalogo, jefatura):
        contenido = ("codigo_institucional;nombre;categoria;unidad;cajonera;tipo;cantidad\n"
                     "8C-0200;Motosierra;MOTORES;B-8;Cajonera 2;unitario;1\n"
                     "8C-0200;Duplicada;MOTORES;B-8;Cajonera 2;unitario;1\n"
                     ";Sin categoría válida;NO EXISTE;B-8;Cajonera 2;unitario;1\n"
                     ";Guantes;MOTORES;B-8;Cabina trasera;granel;30\n")
        resultado = importacion.importar_planilla(SimpleUploadedFile("carga.csv", contenido.encode("utf-8")), jefatura)
        assert len(resultado.registrados) == 2
        assert [r["fila"] for r in resultado.rechazados] == [3, 4]
        assert "ya pertenece" in resultado.rechazados[0]["motivos"][0]


class TestCP04CodigoUnico:
    def test_rechaza_codigo_repetido_sin_distinguir_mayusculas(self, material):
        with pytest.raises(ValidationError, match="Motobomba portátil"):
            services.verificar_codigo("  8c-0112 ")

    def test_codigo_de_elemento_dado_de_baja_no_se_reutiliza(self, material, jefatura):
        material.dar_de_baja("Fin de vida útil", jefatura)
        with pytest.raises(ValidationError, match="dado de baja"):
            services.verificar_codigo("8C-0112")


class TestCP05Busqueda:
    def test_busca_desde_el_segundo_caracter_y_filtra(self, material, catalogo, jefatura):
        services.registrar_material({"codigo_institucional": "8C-0457", "nombre": "Detector multigas",
                                     "categoria": catalogo["hazmat"], "cajonera": catalogo["h8_caj3"],
                                     "tipo": "unitario"}, jefatura)
        assert Material.objects.buscar("d").count() == 2  # un carácter no filtra
        assert list(Material.objects.buscar("multi").values_list("codigo_institucional", flat=True)) == ["8C-0457"]
        assert Material.objects.buscar("0112").get() == material

    def test_lista_por_defecto_solo_activos(self, client, material, jefatura):
        material.dar_de_baja("prueba", jefatura)
        client.force_login(jefatura)
        assert list(client.get(reverse("inventario:lista")).context["materiales"]) == []
        assert len(client.get(reverse("inventario:lista"), {"estado": "todos"}).context["materiales"]) == 1

    def test_categoria_con_elementos_no_se_elimina(self, client, material, administrador):
        client.force_login(administrador)
        client.post(reverse("inventario:eliminar", args=["categoria", material.categoria_id]))
        assert material.categoria.__class__.objects.filter(pk=material.categoria_id).exists()


class TestCP06Movimientos:
    def test_traslado_guarda_origen_destino_y_actualiza_ubicacion(self, material, catalogo, bombero):
        movimiento = material.trasladar(catalogo["caj2"], bombero, "Reorganización")
        material.refresh_from_db()
        assert material.cajonera == catalogo["caj2"]
        assert movimiento.cajonera_origen == catalogo["cabina"] and movimiento.usuario == bombero

    def test_no_se_mueve_a_la_misma_ubicacion_ni_dado_de_baja(self, material, catalogo, jefatura):
        with pytest.raises(ValidationError):
            material.trasladar(catalogo["cabina"], jefatura)
        material.dar_de_baja("prueba", jefatura)
        with pytest.raises(ValidationError):
            material.trasladar(catalogo["caj2"], jefatura)

    def test_cajonera_con_elementos_no_se_elimina(self, client, material, administrador):
        client.force_login(administrador)
        client.post(reverse("inventario:eliminar", args=["cajonera", material.cajonera_id]))
        assert material.cajonera.__class__.objects.filter(pk=material.cajonera_id).exists()


class TestCargaMasivaCreaCatalogos:
    def _cargar(self, contenido, usuario, **kwargs):
        return importacion.importar_planilla(SimpleUploadedFile("carga.csv", contenido.encode("utf-8")), usuario,
                                             **kwargs)

    def test_crea_categorias_unidades_y_cajoneras_que_faltan(self, catalogo, jefatura):
        from inventario.models import Cajonera, Categoria, Unidad

        contenido = ("codigo;nombre;categoria;unidad;cajonera;tipo;cantidad\n"
                     "8C-0300;Botella ERA;Respiración;B-8;CABINA TRIPULACION;unitario;1\n"
                     "8C-0301;Máscara ERA;RESPIRACION;b-8;Cabina  Tripulación;unitario;1\n"
                     ";Vendas;Primeros auxilios;BX-8;Cajonera 1;granel;10\n"
                     "8C-0302;Llave;Herramientas;B-8;Cajonera 2;unitario;1\n")
        resultado = self._cargar(contenido, jefatura)
        assert len(resultado.registrados) == 4 and not resultado.rechazados
        # Sin duplicar por mayúsculas, tildes ni espacios repetidos
        assert Categoria.objects.filter(nombre__iexact="respiración").count() == 1
        assert Cajonera.objects.filter(unidad__codigo="B-8", nombre__icontains="tripula").count() == 1
        assert Unidad.objects.filter(codigo="BX-8").exists()
        assert resultado.unidades_creadas == ["BX-8"]
        assert sorted(resultado.categorias_creadas) == ["Herramientas", "Primeros auxilios", "Respiración"]
        assert resultado.cajoneras_creadas == ["B-8 / CABINA TRIPULACION", "BX-8 / Cajonera 1"]
        assert EventoAuditoria.objects.filter(entidad_afectada="cajonera", accion="alta").count() == 2

    def test_fila_rechazada_no_deja_catalogos_creados(self, catalogo, jefatura):
        from inventario.models import Categoria, Unidad

        contenido = ("codigo;nombre;categoria;unidad;cajonera;tipo\n"
                     ";Sin código;Nueva categoría;NUEVA;Caj 1;unitario\n")
        resultado = self._cargar(contenido, jefatura)
        assert [r["fila"] for r in resultado.rechazados] == [2]
        assert not Categoria.objects.filter(nombre="Nueva categoría").exists()
        assert not Unidad.objects.filter(codigo="NUEVA").exists()
        assert resultado.catalogos_creados == 0

    def test_sin_la_opcion_rechaza_catalogos_inexistentes(self, catalogo, jefatura):
        contenido = ("codigo;nombre;categoria;unidad;cajonera;tipo\n"
                     "8C-0400;Hacha;Herramientas;B-8;Cabina;unitario\n")
        resultado = self._cargar(contenido, jefatura, crear_catalogos=False)
        motivos = resultado.rechazados[0]["motivos"]
        assert "la categoría «Herramientas» no existe" in motivos
        assert "la cajonera «B-8 / Cabina» no existe" in motivos

    def test_la_vista_crea_catalogos_por_defecto(self, client, catalogo, jefatura):
        client.force_login(jefatura)
        contenido = "codigo;nombre;categoria;unidad;cajonera;tipo\n8C-0500;Tablet;Comunicaciones;B-8;Cabina;unitario\n"
        respuesta = client.post(reverse("inventario:importar"), {
            "archivo": SimpleUploadedFile("carga.csv", contenido.encode()), "crear_catalogos": "on"})
        assert respuesta.context["resultado"].catalogos_creados == 2
        assert Material.objects.filter(codigo_institucional="8C-0500").exists()
