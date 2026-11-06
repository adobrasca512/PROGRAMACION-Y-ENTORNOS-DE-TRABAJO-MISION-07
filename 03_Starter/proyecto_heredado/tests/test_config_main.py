"""Pruebas de la configuración por variables de entorno y de la interfaz."""

import pytest

from demanda import main as modulo_main
from demanda.config import (
    RAIZ_PROYECTO,
    RUTA_POR_DEFECTO,
    obtener_factor,
    obtener_ruta_csv,
)


@pytest.fixture(autouse=True)
def entorno_limpio(monkeypatch):
    """Cada prueba empieza sin variables del proyecto ni lectura del .env."""
    monkeypatch.delenv("VENTAS_CSV", raising=False)
    monkeypatch.delenv("FACTOR_DEMANDA", raising=False)
    monkeypatch.setattr(modulo_main, "cargar_entorno", lambda: None)


def test_valores_por_defecto():
    assert obtener_ruta_csv() == RUTA_POR_DEFECTO
    assert obtener_factor() == pytest.approx(1.1)


def test_ruta_relativa_al_proyecto(monkeypatch):
    monkeypatch.setenv("VENTAS_CSV", "data/otro.csv")
    assert obtener_ruta_csv() == (RAIZ_PROYECTO / "data" / "otro.csv").resolve()


def test_ruta_absoluta(monkeypatch, tmp_path):
    monkeypatch.setenv("VENTAS_CSV", str(tmp_path / "v.csv"))
    assert obtener_ruta_csv() == (tmp_path / "v.csv").resolve()


@pytest.mark.parametrize("valor", ["abc", "0", "-2", "nan"])
def test_factor_de_entorno_invalido(monkeypatch, valor):
    monkeypatch.setenv("FACTOR_DEMANDA", valor)
    with pytest.raises(ValueError, match="FACTOR_DEMANDA|factor"):
        obtener_factor()


def test_main_correcto(monkeypatch, tmp_path, capsys):
    ruta = tmp_path / "ventas.csv"
    ruta.write_text("ventas\n10\n20\n31\n", encoding="utf-8")
    monkeypatch.setenv("VENTAS_CSV", str(ruta))
    assert modulo_main.main() == 0
    assert "Demanda prevista: 22.37" in capsys.readouterr().out


def test_main_sin_ventas_avisa_sin_traza(monkeypatch, tmp_path, capsys):
    ruta = tmp_path / "ventas.csv"
    ruta.write_text("ventas\n", encoding="utf-8")
    monkeypatch.setenv("VENTAS_CSV", str(ruta))
    assert modulo_main.main() == 1
    assert "AVISO: No hay ventas registradas" in capsys.readouterr().err
