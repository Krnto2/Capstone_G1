"""Fixtures comunes de las pruebas automatizadas (pytest + pytest-django)."""
import io
from datetime import timedelta

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from accesos.models import Rol, Usuario
from inventario import services as inventario
from inventario.models import Cajonera, Categoria, Unidad
from nucleo.utilidades import hoy
from revisiones.models import AsignacionPlan, PlanRevision, PuntoControl, Revision

CLAVE = "Prueba2026x"


@pytest.fixture(autouse=True)
def _media_temporal(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.SIREMA_RESPALDOS_DIR = tmp_path / "respaldos"
    settings.AXES_ENABLED = False


def _crear_usuario(rut, correo, rol, nombre="Usuario", apellidos="Prueba"):
    usuario = Usuario(rut=rut, correo=correo, nombre=nombre, apellidos=apellidos, rol=Rol.objects.get(nombre=rol))
    usuario.set_password(CLAVE)
    usuario.save()
    return usuario


@pytest.fixture
def administrador(db):
    return _crear_usuario("11.111.111-1", "admin@prueba.cl", Rol.ADMINISTRADOR, "Ana", "Torres")


@pytest.fixture
def jefatura(db):
    return _crear_usuario("12.345.678-5", "jefe@prueba.cl", Rol.JEFATURA, "Carlos", "Muñoz")


@pytest.fixture
def bombero(db):
    return _crear_usuario("15.555.555-6", "bombero@prueba.cl", Rol.BOMBERO, "Juan", "Soto")


@pytest.fixture
def otro_bombero(db):
    return _crear_usuario("16.666.666-6", "otro@prueba.cl", Rol.BOMBERO, "María", "Rivas")


@pytest.fixture
def catalogo(db):
    b8 = Unidad.objects.create(codigo="B-8", nombre="Carro de incendios")
    h8 = Unidad.objects.create(codigo="H-8", nombre="Unidad HazMat")
    return {
        "b8": b8, "h8": h8,
        "cabina": Cajonera.objects.create(unidad=b8, nombre="Cabina trasera"),
        "caj2": Cajonera.objects.create(unidad=b8, nombre="Cajonera 2"),
        "h8_caj3": Cajonera.objects.create(unidad=h8, nombre="Cajonera 3"),
        "motores": Categoria.objects.create(nombre="MOTORES"),
        "hazmat": Categoria.objects.create(nombre="HAZMAT"),
    }


@pytest.fixture
def material(catalogo, jefatura):
    return inventario.registrar_material({
        "codigo_institucional": "8C-0112", "nombre": "Motobomba portátil", "categoria": catalogo["motores"],
        "cajonera": catalogo["cabina"], "tipo": "unitario", "cantidad": 1,
    }, jefatura)


@pytest.fixture
def plan(db):
    plan = PlanRevision.objects.create(nombre="Motobomba", frecuencia_valor=1, frecuencia_unidad="semana",
                                       dias_tolerancia=1, exige_fotografia=False)
    PuntoControl.objects.create(plan=plan, numero_orden=1, descripcion="¿Enciende?", tipo_dato="booleano")
    PuntoControl.objects.create(plan=plan, numero_orden=2, descripcion="Presión de descarga", tipo_dato="numerico",
                                unidad_medida="bar", valor_minimo=6, valor_maximo=10)
    PuntoControl.objects.create(plan=plan, numero_orden=3, descripcion="Mangueras", tipo_dato="seleccion",
                                obligatorio=False)
    return plan


@pytest.fixture
def asignacion(plan, material, bombero):
    return AsignacionPlan.objects.create(plan=plan, material=material, usuario_responsable=bombero,
                                         fecha_inicio=hoy())


@pytest.fixture
def revision(asignacion, bombero):
    return Revision.objects.create(asignacion=asignacion, usuario_responsable=bombero, fecha_programada=hoy(),
                                   fecha_limite=hoy() + timedelta(days=1))


def imagen_prueba(color=(40, 80, 120), tamano=(400, 300), formato="JPEG", nombre="foto.jpg"):
    bufer = io.BytesIO()
    Image.new("RGB", tamano, color).save(bufer, formato)
    tipo = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}[formato]
    return SimpleUploadedFile(nombre, bufer.getvalue(), content_type=tipo)


@pytest.fixture
def imagen():
    return imagen_prueba
