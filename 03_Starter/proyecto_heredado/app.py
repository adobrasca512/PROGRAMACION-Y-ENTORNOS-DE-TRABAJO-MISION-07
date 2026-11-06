"""Punto de entrada compatible con el proyecto original.

La implementación está en el paquete ``src/demanda``. Este módulo la reexporta
para poder ejecutar ``python app.py`` y para las pruebas de ``test_app.py``.
"""

from demanda.calculo import estimar
from demanda.carga import cargar_ventas, convertir_venta, validar_archivo
from demanda.config import RUTA_POR_DEFECTO, obtener_factor, obtener_ruta_csv
from demanda.main import main

__all__ = [
    "RUTA_POR_DEFECTO",
    "cargar_ventas",
    "convertir_venta",
    "estimar",
    "main",
    "obtener_factor",
    "obtener_ruta_csv",
    "validar_archivo",
]

if __name__ == "__main__":
    raise SystemExit(main())
