"""Pruebas de la lectura y validación del CSV (demanda.carga)."""

import pytest

from demanda.carga import DatosInvalidosError, cargar_ventas


@pytest.fixture
def csv_ventas(tmp_path):
    """Crea un CSV temporal con el contenido indicado y devuelve su ruta."""

    def _crear(contenido: str, nombre: str = "ventas.csv", bom: bool = False):
        ruta = tmp_path / nombre
        ruta.write_text(contenido, encoding="utf-8-sig" if bom else "utf-8")
        return ruta

    return _crear


def test_carga_normal(csv_ventas):
    assert cargar_ventas(csv_ventas("ventas\n10\n20\n30\n")) == [10, 20, 30]


def test_carga_con_bom_de_excel(csv_ventas):
    assert cargar_ventas(csv_ventas("ventas\n10\n", bom=True)) == [10]


def test_solo_cabecera_devuelve_lista_vacia(csv_ventas):
    assert cargar_ventas(csv_ventas("ventas\n")) == []


def test_archivo_no_existe(tmp_path):
    with pytest.raises(FileNotFoundError):
        cargar_ventas(tmp_path / "no_existe.csv")


def test_archivo_vacio(csv_ventas):
    with pytest.raises(DatosInvalidosError, match="vacío"):
        cargar_ventas(csv_ventas(""))


def test_extension_incorrecta(csv_ventas):
    with pytest.raises(DatosInvalidosError, match=".csv"):
        cargar_ventas(csv_ventas("ventas\n10\n", nombre="ventas.txt"))


def test_cabecera_incorrecta(csv_ventas):
    with pytest.raises(DatosInvalidosError, match="columna 'ventas'"):
        cargar_ventas(csv_ventas("venta\n10\n"))


@pytest.mark.parametrize(
    ("contenido", "mensaje"),
    [
        ("ventas\n10\nabc\n", "Fila 3: 'abc' no es un número"),
        ("ventas\n   \n", "Fila 2: la venta está vacía"),
        ("ventas\nnan\n", "no es un número válido"),
        ("ventas\ninf\n", "no es un número válido"),
        ("ventas\n-5\n", "negativas"),
        ("ventas\n10.5\n", "decimales"),
        ("ventas\n10,5\n", "coma decimal"),
    ],
    ids=["texto", "celda_vacia", "nan", "inf", "negativo", "decimal", "coma_decimal"],
)
def test_valores_invalidos(csv_ventas, contenido, mensaje):
    with pytest.raises(DatosInvalidosError, match=mensaje):
        cargar_ventas(csv_ventas(contenido))
