"""Entrada de datos: lectura y validación del CSV de ventas."""

import csv
import math
from pathlib import Path

COLUMNA_VENTAS = "ventas"


class DatosInvalidosError(ValueError):
    """El archivo de ventas existe pero su contenido no es válido."""


def validar_archivo(ruta: Path) -> None:
    """Comprueba que la ruta apunte a un archivo .csv existente y no vacío."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo de ventas: {ruta}")
    if not ruta.is_file():
        raise IsADirectoryError(f"La ruta es una carpeta, no un archivo: {ruta}")
    if ruta.suffix.lower() != ".csv":
        raise DatosInvalidosError(f"El archivo debe tener extensión .csv: {ruta}")
    if ruta.stat().st_size == 0:
        raise DatosInvalidosError(f"El archivo está vacío: {ruta}")


def convertir_venta(texto: str | None, fila: int) -> float:
    """Convierte el texto de una celda en una venta válida."""
    if texto is None or not texto.strip():
        raise DatosInvalidosError(f"Fila {fila}: la venta está vacía.")
    try:
        valor = float(texto.strip())
    except ValueError:
        raise DatosInvalidosError(f"Fila {fila}: '{texto}' no es un número.") from None
    if not math.isfinite(valor):
        raise DatosInvalidosError(f"Fila {fila}: '{texto}' no es un número válido.")
    if valor < 0:
        raise DatosInvalidosError(
            f"Fila {fila}: las ventas no pueden ser negativas ({texto})."
        )
    if not valor.is_integer():
        raise DatosInvalidosError(
            f"Fila {fila}: las ventas no pueden tener decimales ({texto})."
        )
    return valor


def cargar_ventas(ruta: Path) -> list[float]:
    """Lee el CSV y devuelve la lista de ventas validadas."""
    validar_archivo(ruta)
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames or COLUMNA_VENTAS not in lector.fieldnames:
            raise DatosInvalidosError(
                f"El CSV debe tener una columna '{COLUMNA_VENTAS}'."
            )
        ventas = []
        # La fila 1 es la cabecera: los datos empiezan en la 2.
        for numero, fila in enumerate(lector, start=2):
            if None in fila:  # columnas de más, p. ej. coma decimal "10,5"
                raise DatosInvalidosError(
                    f"Fila {numero}: tiene más columnas de las esperadas "
                    "(¿usaste coma decimal?)."
                )
            ventas.append(convertir_venta(fila[COLUMNA_VENTAS], numero))
    return ventas
