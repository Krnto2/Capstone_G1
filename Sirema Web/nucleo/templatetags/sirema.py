import os

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.html import format_html

from nucleo.utilidades import formatear_rut

register = template.Library()

ESTADO_REVISION = {
    "pendiente": ("Pendiente", "estado-pendiente"),
    "en_curso": ("En curso", "estado-en-curso"),
    "realizada": ("Realizada", "estado-realizada"),
    "vencida": ("Vencida", "estado-vencida"),
    "no_realizada": ("No realizada", "estado-no-realizada"),
}
RESULTADO = {
    "conforme": ("Conforme", "resultado-conforme", "bi-check-circle"),
    "observacion": ("Observación", "resultado-observacion", "bi-exclamation-triangle"),
    "falla": ("Falla", "resultado-falla", "bi-x-circle"),
}
CRITICIDAD = {
    "alta": ("Alta", "criticidad-alta"),
    "media": ("Media", "criticidad-media"),
    "baja": ("Baja", "criticidad-baja"),
}
ESTADO_HALLAZGO = {
    "abierto": ("Abierto", "estado-vencida"),
    "en_reparacion": ("En reparación", "estado-en-curso"),
    "cerrado": ("Cerrado", "estado-realizada"),
}


@register.filter
def badge_estado(estado):
    texto, clase = ESTADO_REVISION.get(estado, (estado, "estado-pendiente"))
    return format_html('<span class="badge-sirema {}">{}</span>', clase, texto)


@register.filter
def badge_resultado(resultado):
    if not resultado:
        return format_html('<span class="text-body-secondary">{}</span>', "Sin resultado")
    texto, clase, icono = RESULTADO.get(resultado, (resultado, "", "bi-circle"))
    return format_html('<span class="badge-sirema {}"><i class="bi {}" aria-hidden="true"></i> {}</span>',
                       clase, icono, texto)


@register.filter
def badge_criticidad(criticidad):
    texto, clase = CRITICIDAD.get(criticidad, (criticidad, ""))
    return format_html('<span class="badge-sirema {}">{}</span>', clase, texto)


@register.filter
def badge_hallazgo(estado):
    texto, clase = ESTADO_HALLAZGO.get(estado, (estado, ""))
    return format_html('<span class="badge-sirema {}">{}</span>', clase, texto)


@register.filter
def rut(valor):
    return formatear_rut(valor)


@register.filter
def tiene(usuario, codigo):
    return bool(getattr(usuario, "tiene_permiso", None)) and usuario.tiene_permiso(codigo)


@register.filter
def porcentaje(valor, decimales=1):
    if valor is None:
        return "—"
    texto = f"{float(valor):.{int(decimales)}f}".replace(".", ",")
    if texto.endswith(",0") and float(valor) in (0, 100):
        texto = texto[:-2]
    return f"{texto} %"


@register.filter
def numero(valor):
    """Muestra un número decimal con coma y sin ceros sobrantes."""
    if valor is None or valor == "":
        return ""
    texto = f"{valor}"
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto.replace(".", ",")


@register.simple_tag
def estatico(ruta):
    """Como {% static %}, pero en desarrollo agrega la fecha del archivo para que el navegador
    no use una versión antigua en caché. En producción los nombres ya llevan hash (Manifest)."""
    url = static(ruta)
    if settings.DEBUG:
        archivo = finders.find(ruta)
        if archivo:
            url += f"?v={int(os.path.getmtime(archivo))}"
    return url


@register.simple_tag(takes_context=True)
def nav_activo(context, nombres):
    """'active' si la vista actual coincide con alguno de los nombres (admite 'app:*')."""
    coincidencia = getattr(context.get("request"), "resolver_match", None)
    if coincidencia is None:
        return ""
    for nombre in nombres.split(","):
        nombre = nombre.strip()
        if nombre.endswith(":*") and coincidencia.namespace == nombre[:-2]:
            return "active"
        if coincidencia.view_name == nombre:
            return "active"
    return ""


@register.inclusion_tag("componentes/_campo.html")
def campo(campo_formulario, etiqueta=None, ayuda=None, clase=""):
    return {"campo": campo_formulario, "etiqueta": etiqueta, "ayuda": ayuda, "clase": clase}
