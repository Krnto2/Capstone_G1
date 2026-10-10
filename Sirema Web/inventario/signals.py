"""
Señales del inventario (patrón observador).

inventario no importa revisiones: avisa la baja de un elemento con esta señal
y revisiones, que sí conoce el inventario, reacciona cerrando sus asignaciones.
"""
from django.dispatch import Signal

# Argumentos: material, usuario
material_dado_de_baja = Signal()
