"""Tests de app.py (previsión de demanda)."""

import pytest

import app


def crear_csv(carpeta, contenido, nombre="ventas.csv"):
    """Crea un CSV temporal con el contenido indicado y devuelve su ruta."""
    ruta = carpeta / nombre
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


# --- Configuración ---------------------------------------------------------


def test_obtener_ruta_csv_usa_variable_de_entorno(tmp_path, monkeypatch):
    ruta = crear_csv(tmp_path, "ventas\n10\n")
    monkeypatch.setenv("VENTAS_CSV", str(ruta))
    assert app.obtener_ruta_csv() == ruta.resolve()


def test_obtener_ruta_csv_por_defecto(monkeypatch):
    monkeypatch.delenv("VENTAS_CSV", raising=False)
    assert app.obtener_ruta_csv() == app.RUTA_POR_DEFECTO.resolve()


def test_obtener_factor_por_defecto(monkeypatch):
    monkeypatch.delenv("FACTOR_DEMANDA", raising=False)
    assert app.obtener_factor() == 1.1


def test_obtener_factor_desde_variable(monkeypatch):
    monkeypatch.setenv("FACTOR_DEMANDA", "1.5")
    assert app.obtener_factor() == 1.5


@pytest.mark.parametrize("texto", ["abc", "0", "-1", "inf", "nan"])
def test_obtener_factor_invalido(monkeypatch, texto):
    monkeypatch.setenv("FACTOR_DEMANDA", texto)
    with pytest.raises(ValueError):
        app.obtener_factor()


# --- Validación del archivo --------------------------------------------------


def test_validar_archivo_correcto(tmp_path):
    app.validar_archivo(crear_csv(tmp_path, "ventas\n10\n"))  # no lanza error


def test_validar_archivo_no_existe(tmp_path):
    with pytest.raises(FileNotFoundError):
        app.validar_archivo(tmp_path / "no_existe.csv")


def test_validar_archivo_es_carpeta(tmp_path):
    carpeta = tmp_path / "datos.csv"
    carpeta.mkdir()
    with pytest.raises(IsADirectoryError):
        app.validar_archivo(carpeta)


def test_validar_archivo_extension_incorrecta(tmp_path):
    with pytest.raises(ValueError, match="extensión"):
        app.validar_archivo(crear_csv(tmp_path, "ventas\n10\n", "ventas.txt"))


def test_validar_archivo_vacio(tmp_path):
    with pytest.raises(ValueError, match="vacío"):
        app.validar_archivo(crear_csv(tmp_path, ""))


# --- Conversión de cada venta ------------------------------------------------


def test_convertir_venta_correcta():
    assert app.convertir_venta(" 10 ", 2) == 10.0


@pytest.mark.parametrize(
    "texto, mensaje",
    [
        (None, "vacía"),
        ("", "vacía"),
        ("abc", "no es un número"),
        ("inf", "no es un número válido"),
        ("-5", "negativas"),
        ("10.5", "decimales"),
    ],
)
def test_convertir_venta_invalida(texto, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        app.convertir_venta(texto, 3)


def test_convertir_venta_indica_la_fila():
    with pytest.raises(ValueError, match="Fila 7"):
        app.convertir_venta("abc", 7)


# --- Carga del CSV -----------------------------------------------------------


def test_cargar_ventas_correcto(tmp_path):
    ruta = crear_csv(tmp_path, "ventas\n10\n20\n30\n")
    assert app.cargar_ventas(ruta) == [10.0, 20.0, 30.0]


def test_cargar_ventas_solo_cabecera(tmp_path):
    assert app.cargar_ventas(crear_csv(tmp_path, "ventas\n")) == []


def test_cargar_ventas_cabecera_incorrecta(tmp_path):
    with pytest.raises(ValueError, match="columna 'ventas'"):
        app.cargar_ventas(crear_csv(tmp_path, "venta\n10\n"))


def test_cargar_ventas_coma_decimal(tmp_path):
    with pytest.raises(ValueError, match="más columnas"):
        app.cargar_ventas(crear_csv(tmp_path, "ventas\n10,5\n"))


def test_cargar_ventas_valor_no_numerico(tmp_path):
    with pytest.raises(ValueError, match="Fila 3"):
        app.cargar_ventas(crear_csv(tmp_path, "ventas\n10\nabc\n"))


# --- Lógica de negocio -------------------------------------------------------


def test_estimar_con_factor_por_defecto():
    assert app.estimar([10, 20, 30]) == pytest.approx(22.0)


def test_estimar_con_factor_personalizado():
    assert app.estimar([10, 20], factor=2) == pytest.approx(30.0)


def test_estimar_sin_ventas():
    with pytest.raises(ValueError, match="No hay ventas"):
        app.estimar([])


# --- Interfaz (main) ---------------------------------------------------------


def test_main_correcto(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("VENTAS_CSV", str(crear_csv(tmp_path, "ventas\n10\n20\n31\n")))
    monkeypatch.delenv("FACTOR_DEMANDA", raising=False)
    assert app.main() == 0
    assert "Demanda prevista: 22.37" in capsys.readouterr().out


def test_main_sin_ventas_muestra_aviso(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("VENTAS_CSV", str(crear_csv(tmp_path, "ventas\n")))
    assert app.main() == 1
    assert "AVISO: No hay ventas" in capsys.readouterr().err


def test_main_archivo_inexistente(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("VENTAS_CSV", str(tmp_path / "no_existe.csv"))
    assert app.main() == 1
    assert "No se encontró" in capsys.readouterr().err
