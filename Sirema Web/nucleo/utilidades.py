"""Funciones comunes sin dependencias de otras aplicaciones."""
import calendar
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from django.utils import timezone


def hoy():
    """Fecha actual en la hora de Chile continental."""
    return timezone.localdate()


def sumar_meses(fecha, meses):
    mes = fecha.month - 1 + meses
    anio = fecha.year + mes // 12
    mes = mes % 12 + 1
    dia = min(fecha.day, calendar.monthrange(anio, mes)[1])
    return date(anio, mes, dia)


def sumar_periodo(fecha, valor, unidad, veces=1):
    """Suma `veces` períodos de `valor` `unidad` (dia, semana, mes, anio) a `fecha`."""
    total = valor * veces
    if unidad == "dia":
        return fecha + timedelta(days=total)
    if unidad == "semana":
        return fecha + timedelta(weeks=total)
    if unidad == "mes":
        return sumar_meses(fecha, total)
    if unidad == "anio":
        return sumar_meses(fecha, 12 * total)
    raise ValueError(f"Unidad de frecuencia desconocida: {unidad}")


def normalizar_codigo(codigo):
    """RF-04: el código no distingue mayúsculas ni espacios extremos."""
    if codigo is None:
        return None
    codigo = re.sub(r"\s+", " ", str(codigo)).strip().upper()
    return codigo or None


def limpiar_rut(rut):
    return re.sub(r"[^0-9kK]", "", str(rut or "")).upper()


def digito_verificador(cuerpo):
    suma, factor = 0, 2
    for digito in reversed(str(cuerpo)):
        suma += int(digito) * factor
        factor = 2 if factor == 7 else factor + 1
    resto = 11 - suma % 11
    return {11: "0", 10: "K"}.get(resto, str(resto))


def rut_valido(rut):
    rut = limpiar_rut(rut)
    if len(rut) < 2 or not rut[:-1].isdigit():
        return False
    return digito_verificador(rut[:-1]) == rut[-1]


def formatear_rut(rut):
    """12345678K -> 12.345.678-K"""
    rut = limpiar_rut(rut)
    if len(rut) < 2:
        return rut
    cuerpo, dv = rut[:-1], rut[-1]
    cuerpo = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo}-{dv}"


def a_decimal(valor):
    """Convierte '20,9' o '20.9' en Decimal; None si no es un número."""
    if valor is None:
        return None
    texto = str(valor).strip().replace(" ", "")
    if not texto:
        return None
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    else:
        texto = texto.replace(",", ".")
    try:
        numero = Decimal(texto)
    except InvalidOperation:
        return None
    return numero if numero.is_finite() else None


def ip_cliente(request):
    if request is None:
        return None
    reenviada = request.META.get("HTTP_X_FORWARDED_FOR")
    if reenviada:
        return reenviada.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def inicio_fin_mes(anio, mes):
    ultimo = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, 1), date(anio, mes, ultimo)


MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def nombre_mes(anio, mes):
    return f"{MESES[mes - 1].capitalize()} {anio}"
