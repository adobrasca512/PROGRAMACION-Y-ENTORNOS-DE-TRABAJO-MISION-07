"""Pruebas de la lógica de negocio (demanda.calculo)."""

import math

import pytest

from demanda.calculo import estimar, promedio, validar_factor


def test_caso_normal():
    assert estimar([10, 20, 30]) == pytest.approx(22.0)


def test_factor_personalizado():
    assert estimar([10, 20, 30], factor=2) == pytest.approx(40.0)


def test_vacio_lanza_error_claro():
    with pytest.raises(ValueError, match="No hay ventas"):
        estimar([])


def test_negativos_lanzan_error():
    with pytest.raises(ValueError, match="negativas"):
        promedio([10, -5, 20])


@pytest.mark.parametrize("factor", [0, -1, math.nan, math.inf, "1.1", True])
def test_parametro_invalido(factor):
    with pytest.raises(ValueError, match="factor"):
        validar_factor(factor)
