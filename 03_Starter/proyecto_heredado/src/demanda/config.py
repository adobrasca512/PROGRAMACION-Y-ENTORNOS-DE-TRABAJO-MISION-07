"""Configuración externa: variables de entorno y archivo .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

from demanda.calculo import FACTOR_POR_DEFECTO, validar_factor

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_POR_DEFECTO = RAIZ_PROYECTO / "ventas.csv"


def cargar_entorno() -> None:
    """Carga el .env del proyecto si existe (no pisa variables ya definidas)."""
    load_dotenv(RAIZ_PROYECTO / ".env")


def obtener_ruta_csv() -> Path:
    """Ruta del CSV: VENTAS_CSV (relativa al proyecto o absoluta) o la de defecto."""
    valor = os.getenv("VENTAS_CSV", "").strip()
    if not valor:
        return RUTA_POR_DEFECTO
    ruta = Path(valor)
    if not ruta.is_absolute():
        ruta = RAIZ_PROYECTO / ruta
    return ruta.resolve()


def obtener_factor() -> float:
    """Factor de ajuste: FACTOR_DEMANDA o 1.1 por defecto."""
    texto = os.getenv("FACTOR_DEMANDA", "").strip()
    if not texto:
        return FACTOR_POR_DEFECTO
    try:
        factor = float(texto)
    except ValueError:
        raise ValueError(f"FACTOR_DEMANDA debe ser un número: '{texto}'") from None
    return validar_factor(factor)
