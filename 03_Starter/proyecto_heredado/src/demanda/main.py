"""Interfaz de consola: une configuración, carga y cálculo, y muestra el resultado."""

import csv
import sys

from demanda.calculo import estimar, promedio
from demanda.carga import cargar_ventas
from demanda.config import cargar_entorno, obtener_factor, obtener_ruta_csv


def main() -> int:
    """Ejecuta el programa y devuelve el código de salida (0 = correcto)."""
    cargar_entorno()
    try:
        factor = obtener_factor()
        ventas = cargar_ventas(obtener_ruta_csv())
        media = promedio(ventas)
        demanda = estimar(ventas, factor)
    except (OSError, ValueError, csv.Error) as error:
        print(f"AVISO: {error}", file=sys.stderr)
        return 1
    print(f"Ventas leídas: {len(ventas)}")
    print(f"Promedio de ventas: {media:.2f}")
    print(f"Demanda prevista: {demanda:.2f} (promedio x factor {factor:.2f})")
    return 0
