"""
Roles, permisos y usuario técnico «sistema».

Jefatura y Administrador heredan de Bombero (diagrama general de casos de
uso): reciben todos sus permisos más los propios. El rol «consulta» se
eliminó en la Fase 2 porque ningún integrante de la compañía lo cumple.
"""
from django.contrib.auth.hashers import make_password
from django.db import migrations

PERMISOS = [
    # (código, nombre, módulo)
    ("usuario.administrar", "Administrar usuarios y asignar roles", "accesos"),
    ("permiso.administrar", "Administrar permisos por rol", "accesos"),
    ("auditoria.consultar", "Consultar bitácora de auditoría", "accesos"),
    ("material.consultar", "Buscar material y consultar su historial", "inventario"),
    ("material.registrar", "Registrar material y cargar planillas", "inventario"),
    ("material.modificar", "Modificar ficha de material", "inventario"),
    ("material.dar_de_baja", "Dar de baja material", "inventario"),
    ("movimiento.registrar", "Registrar movimiento de material", "inventario"),
    ("catalogo.administrar", "Administrar unidades, cajoneras y categorías", "inventario"),
    ("revision.ejecutar", "Ejecutar sus revisiones asignadas", "revisiones"),
    ("revision.supervisar", "Consultar y reasignar todas las revisiones", "revisiones"),
    ("plan.administrar", "Definir planes y puntos de control", "revisiones"),
    ("asignacion.administrar", "Asignar planes a material", "revisiones"),
    ("fotografia.anular", "Anular fotografías de evidencia", "revisiones"),
    ("hallazgo.gestionar", "Dar seguimiento y cerrar hallazgos", "revisiones"),
    ("panel.consultar", "Consultar panel de cumplimiento", "revisiones"),
    ("reporte.exportar", "Exportar reportes de cumplimiento", "revisiones"),
]

BOMBERO = ["material.consultar", "movimiento.registrar", "revision.ejecutar"]
ROLES = {
    "bombero": ("Voluntario: consulta el inventario, registra traslados y ejecuta sus revisiones.", BOMBERO),
    "jefatura": ("Oficiales: gestionan material, planes, asignaciones, hallazgos y reportes.", BOMBERO + [
        "material.registrar", "material.modificar", "material.dar_de_baja", "revision.supervisar",
        "plan.administrar", "asignacion.administrar", "fotografia.anular", "hallazgo.gestionar",
        "panel.consultar", "reporte.exportar"]),
    "administrador": ("Bombero designado: administra usuarios, permisos, catálogos y bitácora.", BOMBERO + [
        "usuario.administrar", "permiso.administrar", "auditoria.consultar", "catalogo.administrar"]),
}


def cargar(apps, schema_editor):
    Rol = apps.get_model("accesos", "Rol")
    Permiso = apps.get_model("accesos", "Permiso")
    RolPermiso = apps.get_model("accesos", "RolPermiso")
    Usuario = apps.get_model("accesos", "Usuario")

    permisos = {}
    for codigo, nombre, modulo in PERMISOS:
        permisos[codigo], _ = Permiso.objects.get_or_create(codigo=codigo, defaults={"nombre": nombre,
                                                                                   "modulo": modulo})
    for nombre, (descripcion, codigos) in ROLES.items():
        rol, _ = Rol.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})
        existentes = set(RolPermiso.objects.filter(rol=rol).values_list("permiso_id", flat=True))
        RolPermiso.objects.bulk_create([RolPermiso(rol=rol, permiso=permisos[c]) for c in codigos
                                        if permisos[c].pk not in existentes])

    # Las acciones automáticas se atribuyen a «sistema», sin credenciales (DAS 4.2.5).
    if not Usuario.objects.filter(correo="sistema@sirema.local").exists():
        Usuario.objects.create(correo="sistema@sirema.local", rut="SISTEMA", nombre="Sistema", apellidos="SIREMA",
                               rol=Rol.objects.get(nombre="bombero"), activo=False, password=make_password(None))


class Migration(migrations.Migration):
    dependencies = [("accesos", "0001_initial")]
    operations = [migrations.RunPython(cargar, migrations.RunPython.noop)]
