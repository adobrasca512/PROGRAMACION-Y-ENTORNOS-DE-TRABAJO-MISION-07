"""Estimación de la demanda de un producto a partir de su histórico de ventas."""

import csv
import math
import os
import sys
from pathlib import Path

RUTA_POR_DEFECTO = Path(__file__).parent / "ventas.csv"
COLUMNA_VENTAS = "ventas"
FACTOR_POR_DEFECTO = 1.1


# --- Configuración ---------------------------------------------------------


def obtener_ruta_csv() -> Path:
    """Devuelve la ruta del CSV (variable VENTAS_CSV o la ruta por defecto)."""
    ruta = Path(os.getenv("VENTAS_CSV", RUTA_POR_DEFECTO)).resolve()
    validar_archivo(ruta)
    return ruta


def obtener_factor() -> float:
    """Devuelve el factor de ajuste (variable FACTOR_DEMANDA o 1.1)."""
    texto = os.getenv("FACTOR_DEMANDA", str(FACTOR_POR_DEFECTO))
    try:
        factor = float(texto)
    except ValueError:
        raise ValueError(f"FACTOR_DEMANDA debe ser un número: '{texto}'") from None
    if not math.isfinite(factor) or factor <= 0:
        raise ValueError(f"FACTOR_DEMANDA debe ser mayor que 0: '{texto}'")
    return factor


# --- Carga y validación de datos --------------------------------------------


def validar_archivo(ruta: Path) -> None:
    """Comprueba que la ruta apunte a un archivo .csv existente y no vacío."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo de ventas: {ruta}")
    if not ruta.is_file():
        raise IsADirectoryError(f"La ruta es una carpeta, no un archivo: {ruta}")
    if ruta.suffix.lower() != ".csv":
        raise ValueError(f"El archivo debe tener extensión .csv: {ruta}")
    if ruta.stat().st_size == 0:
        raise ValueError(f"El archivo está vacío: {ruta}")


def convertir_venta(texto: str | None, fila: int) -> float:
    """Convierte el texto de una celda en una venta válida."""
    if texto is None or not texto.strip():
        raise ValueError(f"Fila {fila}: la venta está vacía.")
    try:
        valor = float(texto.strip())
    except ValueError:
        raise ValueError(f"Fila {fila}: '{texto}' no es un número.") from None
    if not math.isfinite(valor):
        raise ValueError(f"Fila {fila}: '{texto}' no es un número válido.")
    if valor < 0:
        raise ValueError(f"Fila {fila}: las ventas no pueden ser negativas ({texto}).")
    if not valor.is_integer():
        raise ValueError(
            f"Fila {fila}: las ventas no pueden tener decimales ({texto})."
        )
    return valor


def cargar_ventas(ruta: Path) -> list[float]:
    """Lee el CSV y devuelve la lista de ventas validadas."""
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames or COLUMNA_VENTAS not in lector.fieldnames:
            raise ValueError(f"El CSV debe tener una columna '{COLUMNA_VENTAS}'.")
        ventas = []
        # La fila 1 es la cabecera, los datos empiezan en la 2
        for numero, fila in enumerate(lector, start=2):
            if None in fila:  # columnas de más, p. ej. coma decimal "10,5"
                raise ValueError(
                    f"Fila {numero}: tiene más columnas de las esperadas "
                    "(¿usaste coma decimal?)."
                )
            ventas.append(convertir_venta(fila[COLUMNA_VENTAS], numero))
    return ventas


# --- Lógica de negocio -------------------------------------------------------


def estimar(valores: list[float], factor: float = FACTOR_POR_DEFECTO) -> float:
    """Calcula la demanda prevista: media de las ventas multiplicada por el factor."""
    if not valores:
        raise ValueError("No hay ventas registradas para calcular la demanda.")
    return sum(valores) / len(valores) * factor


# --- Interfaz ----------------------------------------------------------------


def main() -> int:
    """Ejecuta el programa y devuelve el código de salida."""
    try:
        factor = obtener_factor()
        ventas = cargar_ventas(obtener_ruta_csv())
        demanda = estimar(ventas, factor)
    except (OSError, ValueError, csv.Error) as error:
        print(f"AVISO: {error}", file=sys.stderr)
        return 1
    print(f"Demanda prevista: {demanda:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
