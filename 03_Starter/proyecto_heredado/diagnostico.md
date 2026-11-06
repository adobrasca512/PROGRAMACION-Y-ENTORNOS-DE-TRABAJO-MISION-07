# Diagnóstico del proyecto heredado

**Pareja:** Adilem Dobras Castillo · Boris Castellanos Matamoros
**Fecha:** 06/11/2026 · **Entorno:** Windows 11, Python 3.12.0
**Código analizado:** `app.py` original (commit `2726754`), ejecutado con `python app.py`.

```python
import os
import csv

ARCHIVO = 'ventas.csv'

def estimar(valores):
    return sum(valores) / len(valores) * 1.1

def ejecutar():
    with open(ARCHIVO) as f:
        filas = list(csv.DictReader(f))
    ventas = [float(fila['ventas']) for fila in filas]
    print('Demanda prevista:', estimar(ventas))
```

## 1. Fallos iniciales registrados

| Escenario | Contenido del CSV | Salida obtenida |
|---|---|---|
| Datos originales | `10, 20, 30` | `Demanda prevista: 22.0` (correcto) |
| CSV sin ventas | solo cabecera | `ZeroDivisionError: division by zero` |
| Valor no numérico | `10, abc, 30` | `ValueError: could not convert string to float: 'abc'` |
| Separador incorrecto | `10;5` | `ValueError: could not convert string to float: '10;5'` |
| Coma decimal | `10,5` | `Demanda prevista: 16.5` (descarta el `5` sin avisar) |
| Valores especiales | `nan` / `inf` | `Demanda prevista: nan` / `inf` |
| Ventas negativas | `-10, -20` | `Demanda prevista: -16.5` (dato imposible aceptado) |
| Cabecera distinta | columna `venta` | `KeyError: 'ventas'` |
| CSV guardado con Excel (UTF-8 BOM) | cabecera `ventas` | `KeyError: 'ventas'` |
| Ejecutar desde otra carpeta | — | `FileNotFoundError: ... 'ventas.csv'` |
| Media con decimales | `10, 20, 31` | `Demanda prevista: 22.366666666666667` |

## 2. Top 4 de problemas

| # | Problema | Síntoma | Causa | Corrección propuesta |
|---|---|---|---|---|
| P1 | CSV sin ventas | El programa termina con `ZeroDivisionError`. | `estimar()` divide entre `len(valores)` sin comprobar que haya datos. | Comprobar la lista vacía y mostrar un aviso claro en lugar de la traza. |
| P2 | Ruta del CSV fija y dependiente del directorio | `FileNotFoundError` al ejecutar desde otra carpeta. | `ARCHIVO = 'ventas.csv'` está en el código y se resuelve respecto al directorio actual. | Ruta configurable con la variable de entorno `VENTAS_CSV`; valor por defecto relativo al proyecto (`pathlib`). |
| P3 | Datos de entrada sin validar | `ValueError`/`KeyError` con traza; negativos, `nan` y coma decimal dan resultados falsos sin avisar. | `float(fila['ventas'])` sin control de errores, de rango ni de cabecera; `open()` sin `encoding`. | Validar cabecera y cada fila (vacía, no numérica, no finita, negativa, columnas de más) e indicar la fila con el error. |
| P4 | Lógica, E/S y configuración mezcladas; sin pruebas ni entorno | No se puede probar el cálculo aislado; no hay `requirements.txt`, `.gitignore` ni tests. | Todo en una función; factor `1.1` como número mágico; `import os` sin uso. | Paquete en `src/` con módulos de configuración, carga, cálculo e interfaz; factor configurable (`FACTOR_DEMANDA`); pytest; `.venv`. |

## 3. Observaciones adicionales del equipo

| # | Observación | Propuesta | Relación |
|---|---|---|---|
| 1 | La ruta del CSV no debe estar en el código | Ruta relativa o absoluta configurable | P2 |
| 2 | Validar ventas no numéricas | Validación por fila con mensaje claro | P3 |
| 3 | Usar una base de datos en vez de CSV | Aislar el acceso a datos; SQLite como evolución futura | Mejora |
| 4 | Separar carga y cálculo; menú de opciones | Módulos separados; menú como ampliación | P4 |
| 5 | Resultados con muchos decimales | Redondear a 2 decimales al mostrar | Usabilidad |
| 6 | Si no hay ventas, alertar en vez de fallar | Aviso controlado al usuario | P1 |

## 4. Estado tras el rescate

Todos los escenarios de la tabla 1 producen ahora un mensaje `AVISO: ...` claro (sin traza) o el resultado correcto. Cada caso está cubierto por una prueba en `tests/`.
