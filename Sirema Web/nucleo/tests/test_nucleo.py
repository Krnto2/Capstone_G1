from datetime import date
from decimal import Decimal

import pytest

from nucleo.almacenamiento import ErrorAlmacenamiento, ServicioAlmacenamiento
from nucleo.utilidades import a_decimal, formatear_rut, normalizar_codigo, rut_valido, sumar_periodo


class TestUtilidades:
    def test_rut_valido_y_formato(self):
        assert rut_valido("12.345.678-5")
        assert rut_valido("11111111-1")
        assert not rut_valido("12.345.678-0")
        assert formatear_rut("123456785") == "12.345.678-5"

    def test_codigo_sin_mayusculas_ni_espacios_extremos(self):
        assert normalizar_codigo("  8c-0112 ") == "8C-0112"
        assert normalizar_codigo("   ") is None

    def test_sumar_periodo_ajusta_fin_de_mes(self):
        assert sumar_periodo(date(2026, 1, 31), 1, "mes") == date(2026, 2, 28)
        assert sumar_periodo(date(2026, 10, 9), 2, "semana") == date(2026, 10, 23)
        assert sumar_periodo(date(2024, 2, 29), 1, "anio") == date(2025, 2, 28)

    def test_a_decimal_acepta_coma(self):
        assert a_decimal("20,9") == Decimal("20.9")
        assert a_decimal("1.234,5") == Decimal("1234.5")
        assert a_decimal("abc") is None


class TestAlmacenamiento:
    def test_guarda_redimensiona_y_calcula_hash(self, settings, imagen):
        servicio = ServicioAlmacenamiento()
        guardado = servicio.guardar(imagen(tamano=(4000, 3000), formato="PNG", nombre="grande.png"))
        assert guardado.tipo_mime == "image/jpeg"
        assert guardado.tamano_bytes <= settings.SIREMA_FOTO_SALIDA_MAX_BYTES
        assert len(guardado.hash_sha256) == 64
        assert servicio.ruta_absoluta(guardado.ruta).exists()

    def test_rechaza_archivos_que_no_son_imagen(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        with pytest.raises(ErrorAlmacenamiento):
            ServicioAlmacenamiento().guardar(SimpleUploadedFile("x.jpg", b"no soy una imagen"))

    def test_rechaza_archivos_sobre_10_mb(self, settings, imagen):
        settings.SIREMA_FOTO_MAX_BYTES = 100
        with pytest.raises(ErrorAlmacenamiento, match="10 MB"):
            ServicioAlmacenamiento().guardar(imagen())

    def test_no_permite_rutas_fuera_del_volumen(self):
        with pytest.raises(ErrorAlmacenamiento):
            ServicioAlmacenamiento().ruta_absoluta("../../etc/passwd")
