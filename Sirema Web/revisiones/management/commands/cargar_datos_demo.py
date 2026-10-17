"""
Carga datos de demostración FICTICIOS para probar SIREMA (no usar en producción).

    python manage.py cargar_datos_demo

Crea unidades, cajoneras, categorías, material, planes, asignaciones e
historial de revisiones de las últimas semanas, con hallazgos y avisos.

Los usuarios y su contraseña están en accesos/demo.py y en el README
(sección «Usuarios de demostración»).
"""
import io
import random
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw

from accesos.demo import CONTRASENA_DEMO, USUARIOS_DEMO
from accesos.models import Rol, Usuario
from inventario import services as inventario
from inventario.models import Cajonera, Categoria, Material, Unidad
from nucleo.almacenamiento import ServicioAlmacenamiento
from nucleo.enums import EstadoRevision, ResultadoControl, TipoDatoPunto
from nucleo.utilidades import digito_verificador, formatear_rut, hoy
from revisiones.models import (AsignacionPlan, Fotografia, Hallazgo, Notificacion, PlanRevision, PuntoControl,
                               ResultadoPunto)
from revisiones.programador import ProgramadorRevisiones

CONTRASENA = CONTRASENA_DEMO
USUARIOS = USUARIOS_DEMO

UNIDADES = [
    ("B-8", "Carro de incendios", "carro", ["Cabina trasera", "Cajonera 1", "Cajonera 2", "Cajonera 3", "Cajonera 4"]),
    ("H-8", "Unidad HazMat", "carro", ["Cabina", "Cajonera 1", "Cajonera 2", "Cajonera 3"]),
    ("F-8", "Carro de rescate", "carro", ["Cajonera 1", "Cajonera 2", "Techo"]),
    ("BOD", "Bodega del cuartel", "bodega", ["Estante A", "Estante B"]),
]

CATEGORIAS = [
    ("AGUA", "Material de agua y bombeo"), ("ERA", "Equipos de respiración autónoma"),
    ("HAZMAT", "Materiales peligrosos y medición de gases"), ("MOTORES", "Equipos con motor de combustión"),
    ("RESCATE", "Herramientas hidráulicas y de rescate"), ("ELECTRICIDAD", "Generación e iluminación"),
    ("PROTECCIÓN", "Elementos de protección personal"),
]

MATERIAL = [
    # código, nombre, categoría, unidad, cajonera, marca, modelo
    ("8C-0112", "Motobomba portátil", "MOTORES", "B-8", "Cabina trasera", "Honda", "WX15"),
    ("8C-0457", "Detector multigas", "HAZMAT", "H-8", "Cajonera 3", "MSA", "Altair 4XR"),
    ("8C-0233", "Motosierra de rescate", "RESCATE", "B-8", "Cajonera 2", "Stihl", "MS 462 R"),
    ("8C-0390", "Generador eléctrico", "ELECTRICIDAD", "F-8", "Cajonera 1", "Honda", "EU22i"),
    ("8C-0101", "Ventilador de presión positiva", "MOTORES", "B-8", "Cajonera 4", "Tempest", "GX200"),
    ("8C-0305", "Equipo de corte hidráulico", "RESCATE", "F-8", "Cajonera 2", "Holmatro", "CU 4050"),
    ("8C-0458", "Detector monogas H2S", "HAZMAT", "H-8", "Cajonera 3", "Dräger", "Pac 6500"),
    ("8C-0120", "Motobomba de achique", "AGUA", "BOD", "Estante A", "Koshin", "SEV-50X"),
    ("8C-0510", "Equipo de respiración autónoma", "ERA", "B-8", "Cabina trasera", "MSA", "G1"),
    ("8C-0511", "Equipo de respiración autónoma", "ERA", "B-8", "Cabina trasera", "MSA", "G1"),
    ("8C-0612", "Separador hidráulico", "RESCATE", "F-8", "Cajonera 2", "Holmatro", "SP 4240"),
    ("8C-0701", "Torre de iluminación portátil", "ELECTRICIDAD", "F-8", "Techo", "Peli", "9500"),
    ("8C-0215", "Pitón regulable 50 mm", "AGUA", "B-8", "Cajonera 1", "Akron", "Turbojet"),
    ("8C-0216", "Pitón regulable 70 mm", "AGUA", "B-8", "Cajonera 1", "Akron", "Turbojet"),
]

PLANES = {
    "Motobomba": dict(frecuencia_valor=1, frecuencia_unidad="semana", dias_tolerancia=1, exige_fotografia=True,
                      descripcion="Encender en zona ventilada. Usar protección auditiva. Revisar según manual Honda WX15.",
                      puntos=[("¿Nivel de combustible sobre la mitad?", "booleano", None, None, None, True, False),
                              ("¿Enciende en menos de tres intentos?", "booleano", None, None, None, True, False),
                              ("Presión de descarga", "numerico", "bar", "6", "10", True, False),
                              ("Estado de mangueras de succión", "seleccion", None, None, None, True, False),
                              ("¿Sin fugas de aceite?", "booleano", None, None, None, True, False)]),
    "Detector de gases": dict(frecuencia_valor=1, frecuencia_unidad="mes", dias_tolerancia=2, exige_fotografia=True,
                              descripcion="Realizar la prueba en aire limpio, fuera del cuartel. Registrar la lectura "
                                          "estable tras 60 segundos.",
                              puntos=[("Carga de batería", "numerico", "%", "50", "100", True, False),
                                      ("Prueba de alarma sonora y visual", "booleano", None, None, None, True, False),
                                      ("Lectura de O₂ en aire limpio", "numerico", "% vol", "20.5", "21", True, False),
                                      ("Lectura de CO en aire limpio", "numerico", "ppm", "0", "5", True, True),
                                      ("Lectura de H₂S en aire limpio", "numerico", "ppm", "0", "1", True, False),
                                      ("Lectura de LEL en aire limpio", "numerico", "%", "0", "1", True, False)]),
    "Motosierra": dict(frecuencia_valor=1, frecuencia_unidad="semana", dias_tolerancia=1, exige_fotografia=False,
                       descripcion="Verificar con el freno de cadena activado.",
                       puntos=[("¿Nivel de mezcla y aceite de cadena correctos?", "booleano", None, None, None, True,
                                False),
                               ("Tensión de la cadena", "seleccion", None, None, None, True, False),
                               ("Afilado y estado de eslabones", "seleccion", None, None, None, True, True),
                               ("¿Enciende y acelera sin fallas?", "booleano", None, None, None, True, False)]),
    "Generador": dict(frecuencia_valor=2, frecuencia_unidad="semana", dias_tolerancia=2, exige_fotografia=False,
                      descripcion="Conectar la carga de prueba (foco de 500 W) durante 5 minutos.",
                      puntos=[("¿Nivel de aceite correcto?", "booleano", None, None, None, True, False),
                              ("¿Enciende sin fallas?", "booleano", None, None, None, True, False),
                              ("Voltaje de salida", "numerico", "V", "210", "230", True, False),
                              ("Horómetro", "texto", None, None, None, False, False)]),
    "Herramienta hidráulica": dict(frecuencia_valor=1, frecuencia_unidad="mes", dias_tolerancia=3,
                                   exige_fotografia=False,
                                   descripcion="Revisar acoples y mangueras antes de operar la herramienta.",
                                   puntos=[("¿Acoples sin fugas?", "booleano", None, None, None, True, False),
                                           ("Estado de cuchillas o puntas", "seleccion", None, None, None, True, False),
                                           ("Presión de trabajo de la central", "numerico", "bar", "600", "720",
                                            True, False)]),
}

ASIGNACIONES = [
    # código, plan, correo responsable, semanas atrás de inicio
    ("8C-0112", "Motobomba", "j.soto@sirema.local", 8),
    ("8C-0457", "Detector de gases", "j.soto@sirema.local", 12),
    ("8C-0233", "Motosierra", "j.soto@sirema.local", 8),
    ("8C-0390", "Generador", "j.soto@sirema.local", 8),
    ("8C-0101", "Motobomba", "m.rivas@sirema.local", 8),
    ("8C-0305", "Herramienta hidráulica", "p.lagos@sirema.local", 12),
    ("8C-0458", "Detector de gases", "m.rivas@sirema.local", 12),
    ("8C-0120", "Motobomba", "p.lagos@sirema.local", 6),
    ("8C-0612", "Herramienta hidráulica", "p.lagos@sirema.local", 12),
]


class Command(BaseCommand):
    help = "Carga datos de demostración ficticios (usuarios, inventario, planes e historial)."

    def handle(self, *args, **opciones):
        if Unidad.objects.filter(codigo="B-8").exists():
            self.stdout.write(self.style.WARNING("Los datos de demostración ya están cargados."))
            return
        random.seed(8)
        self.almacenamiento = ServicioAlmacenamiento()
        self.contador_fotos = 0
        with transaction.atomic():
            usuarios = self._usuarios()
            self._inventario(usuarios["jefatura@sirema.local"])
            planes = self._planes()
            self._historial(usuarios, planes)
        resumen = ProgramadorRevisiones().ejecutar()
        # Los avisos de las semanas anteriores se dan por leídos para que la demo sea realista.
        hace_dos_dias = timezone.now() - timedelta(days=2)
        Notificacion.objects.filter(revision__fecha_programada__lt=hoy() - timedelta(days=2)).update(
            leida=True, fecha_lectura=hace_dos_dias)
        self.stdout.write(self.style.SUCCESS(f"Datos de demostración cargados. Programador: {resumen}."))
        self.stdout.write(f"Ingrese con jefatura@sirema.local, j.soto@sirema.local o admin@sirema.local "
                          f"(contraseña: {CONTRASENA}).")

    def _usuarios(self):
        usuarios = {}
        for cuerpo, nombre, apellidos, correo, rol in USUARIOS:
            usuario = Usuario.objects.filter(correo=correo).first()
            if usuario is None:
                usuario = Usuario(rut=formatear_rut(cuerpo + digito_verificador(cuerpo)), nombre=nombre,
                                  apellidos=apellidos, correo=correo, telefono="+56 9 5555 0000",
                                  rol=Rol.objects.get(nombre=rol))
                usuario.set_password(CONTRASENA)
                usuario.save()
            usuarios[correo] = usuario
        return usuarios

    def _inventario(self, jefatura):
        for codigo, nombre, tipo, cajoneras in UNIDADES:
            unidad = Unidad.objects.create(codigo=codigo, nombre=nombre, tipo=tipo)
            for orden, cajonera in enumerate(cajoneras, start=1):
                Cajonera.objects.create(unidad=unidad, nombre=cajonera, orden=orden)
        for nombre, descripcion in CATEGORIAS:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
        for codigo, nombre, categoria, unidad, cajonera, marca, modelo in MATERIAL:
            inventario.registrar_material({
                "codigo_institucional": codigo, "nombre": nombre, "categoria": Categoria.objects.get(nombre=categoria),
                "cajonera": Cajonera.objects.get(unidad__codigo=unidad, nombre=cajonera), "tipo": "unitario",
                "cantidad": 1, "marca": marca, "modelo": modelo,
            }, jefatura)
        inventario.registrar_material({
            "codigo_institucional": None, "nombre": "Guantes de nitrilo (caja)",
            "categoria": Categoria.objects.get(nombre="PROTECCIÓN"),
            "cajonera": Cajonera.objects.get(unidad__codigo="BOD", nombre="Estante B"), "tipo": "granel",
            "cantidad": 12, "observaciones": "Material a granel: sin código institucional.",
        }, jefatura)

    def _planes(self):
        planes = {}
        for nombre, datos in PLANES.items():
            datos = dict(datos)
            puntos = datos.pop("puntos")
            plan = PlanRevision.objects.create(nombre=nombre, **datos)
            for orden, (desc, tipo, unidad, minimo, maximo, obligatorio, foto) in enumerate(puntos, start=1):
                PuntoControl.objects.create(plan=plan, numero_orden=orden, descripcion=desc, tipo_dato=tipo,
                                            unidad_medida=unidad, valor_minimo=Decimal(minimo) if minimo else None,
                                            valor_maximo=Decimal(maximo) if maximo else None,
                                            obligatorio=obligatorio, exige_fotografia=foto)
            planes[nombre] = plan
        return planes

    def _foto(self, revision, usuario, punto=None, momento=None):
        self.contador_fotos += 1
        imagen = Image.new("RGB", (640, 480), (random.randint(40, 90), random.randint(60, 110), random.randint(80, 140)))
        dibujo = ImageDraw.Draw(imagen)
        dibujo.rectangle([20, 20, 620, 460], outline=(140, 200, 236), width=6)
        dibujo.text((40, 40), f"SIREMA demo #{self.contador_fotos}", fill=(255, 255, 255))
        dibujo.text((40, 70), revision.material.nombre, fill=(255, 255, 255))
        for _ in range(60):
            x, y = random.randint(40, 600), random.randint(110, 440)
            dibujo.ellipse([x, y, x + 8, y + 8], fill=(random.randint(0, 255), 200, 120))
        bufer = io.BytesIO()
        imagen.save(bufer, "JPEG", quality=80)
        guardado = self.almacenamiento.guardar(SimpleUploadedFile("demo.jpg", bufer.getvalue(), "image/jpeg"))
        Fotografia.objects.create(
            id=guardado.id, revision=revision, punto=punto, usuario=usuario, nombre_archivo=f"IMG_{self.contador_fotos:04d}.jpg",
            ruta_almacenamiento=guardado.ruta, tipo_mime=guardado.tipo_mime, tamano_bytes=guardado.tamano_bytes,
            hash_sha256=guardado.hash_sha256, fecha_hora_captura=momento, fecha_hora_carga=momento,
        )

    def _valor(self, punto, falla=False):
        if punto.tipo_dato == TipoDatoPunto.NUMERICO:
            minimo, maximo = float(punto.valor_minimo or 0), float(punto.valor_maximo or 100)
            if falla:
                return f"{maximo + (maximo - minimo) * 0.6 + 1:.1f}".rstrip("0").rstrip(".")
            return f"{random.uniform(minimo, maximo):.1f}".rstrip("0").rstrip(".")
        if punto.tipo_dato == TipoDatoPunto.BOOLEANO:
            return "No" if falla else "Sí"
        if punto.tipo_dato == TipoDatoPunto.TEXTO:
            return f"{random.randint(120, 480)} h"
        return None

    def _ejecutar(self, revision, usuario, cuando, tipo):
        """tipo: conforme, observacion o falla."""
        puntos = list(revision.plan.puntos.all())
        punto_raro = random.choice(puntos)
        if revision.material.codigo_institucional == "8C-0457" and tipo == "falla":
            punto_raro = next(p for p in puntos if "CO" in p.descripcion)
        inicio = cuando
        for i, punto in enumerate(puntos):
            resultado, observacion, falla = ResultadoControl.CONFORME, None, False
            if punto == punto_raro and tipo != "conforme":
                resultado = ResultadoControl(tipo)
                falla = tipo == "falla"
                observacion = ("El sensor de CO no vuelve a cero tras la calibración." if falla and "CO" in punto.descripcion
                               else "Cadena con desgaste en eslabones." if falla
                               else "Leve suciedad; se limpió en el lugar.")
            ResultadoPunto.objects.create(revision=revision, punto=punto, resultado=resultado,
                                          valor_registrado=self._valor(punto, falla), observacion=observacion,
                                          fecha_hora_registro=inicio + timedelta(minutes=2 * i + 1))
            if punto.exige_fotografia:
                self._foto(revision, usuario, punto, inicio + timedelta(minutes=2 * i + 1))
        if revision.plan.exige_fotografia:
            self._foto(revision, usuario, None, inicio + timedelta(minutes=2 * len(puntos) + 1))
        revision.estado = EstadoRevision.REALIZADA
        revision.usuario_ejecutor = usuario
        revision.fecha_hora_inicio = inicio
        revision.fecha_hora_termino = inicio + timedelta(minutes=2 * len(puntos) + 3)
        revision.resultado_global = revision.calcular_resultado_global()
        revision.save()
        return revision

    def _historial(self, usuarios, planes):
        hoy_ = hoy()
        zona = timezone.get_current_timezone()
        asignaciones = []
        for codigo, plan, correo, semanas in ASIGNACIONES:
            asignaciones.append(AsignacionPlan.objects.create(
                plan=planes[plan], material=Material.objects.get(codigo_institucional=codigo),
                usuario_responsable=usuarios[correo], fecha_inicio=hoy_ - timedelta(weeks=semanas)))
        programador = ProgramadorRevisiones(fecha=hoy_)
        for asignacion in asignaciones:
            programador.generar_para(asignacion)

        jefatura = usuarios["jefatura@sirema.local"]
        for asignacion in asignaciones:
            for revision in asignacion.revisiones.order_by("fecha_programada"):
                if revision.fecha_limite >= hoy_:
                    continue  # pendientes: las ejecutará el bombero
                azar = random.random()
                if azar < 0.06:
                    continue  # quedará vencida
                demora = random.randint(0, (revision.fecha_limite - revision.fecha_programada).days)
                if azar > 0.94:
                    demora += 2  # realizada fuera de plazo
                dia = min(revision.fecha_programada + timedelta(days=demora), hoy_ - timedelta(days=1))
                cuando = datetime.combine(dia, time(random.randint(9, 19), random.randint(0, 59)), zona)
                tipo = "observacion" if random.random() < 0.12 else "conforme"
                self._ejecutar(revision, revision.usuario_responsable, cuando, tipo)

        # Hallazgos coherentes con el prototipo (D1 y M4).
        casos = [("8C-0457", "Sensor de CO marca 8 ppm en aire limpio y no vuelve a cero. Se retira el equipo de la "
                             "unidad H-8 hasta su calibración.", "alta", None),
                 ("8C-0233", "Cadena con desgaste en eslabones; requiere reemplazo.", "media", None),
                 ("8C-0305", "Fuga leve en acople de la manguera de presión.", "baja",
                  "Se reemplazó la junta tórica del acople y se probó sin fugas.")]
        for codigo, descripcion, criticidad, acciones in casos:
            revision = (AsignacionPlan.objects.get(material__codigo_institucional=codigo).revisiones
                        .filter(fecha_limite__lt=hoy_).order_by("-fecha_programada").first())
            if revision is None:
                continue
            if revision.estado == EstadoRevision.REALIZADA:
                # Primero las fotos: fk_foto_resultado (RESTRICT) impide borrar un resultado con fotos.
                revision.fotografias.all().delete()
                revision.resultados.all().delete()
            cuando = datetime.combine(min(revision.fecha_limite, hoy_ - timedelta(days=1)), time(10, 30), zona)
            self._ejecutar(revision, revision.usuario_responsable, cuando, "falla")
            hallazgo = Hallazgo.objects.create(revision=revision, descripcion=descripcion, criticidad=criticidad,
                                               fecha_apertura=revision.fecha_hora_termino)
            if acciones:
                hallazgo.cerrar(acciones, jefatura)
