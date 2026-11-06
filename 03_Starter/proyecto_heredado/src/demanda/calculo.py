"""Lógica de negocio: funciones puras, sin leer archivos ni imprimir."""

import math

FACTOR_POR_DEFECTO = 1.1


def validar_factor(factor: float) -> float:
    """Comprueba que el factor de ajuste sea un número finito mayor que 0."""
    if isinstance(factor, bool) or not isinstance(factor, int | float):
        raise ValueError(f"El factor debe ser un número: {factor!r}")
    if not math.isfinite(factor) or factor <= 0:
        raise ValueError(f"El factor debe ser mayor que 0: {factor}")
    return float(factor)


def promedio(valores: list[float]) -> float:
    """Media de las ventas. Falla si no hay ventas o alguna es negativa."""
    if not valores:
        raise ValueError("No hay ventas registradas para calcular la demanda.")
    if any(v < 0 for v in valores):
        raise ValueError("Las ventas no pueden ser negativas.")
    return sum(valores) / len(valores)


def estimar(valores: list[float], factor: float = FACTOR_POR_DEFECTO) -> float:
    """Demanda prevista: promedio de las ventas multiplicado por el factor."""
    return promedio(valores) * validar_factor(factor)
