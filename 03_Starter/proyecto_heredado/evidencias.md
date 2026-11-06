# Evidencias — pareja: Adilem Dobras Castillo · Boris Castellanos Matamoros

## Diagnóstico

Detalle completo en [`diagnostico.md`](diagnostico.md).

| Problema | Cómo se reproduce | Causa | Solución |
|---|---|---|---|
| P1. CSV sin ventas | CSV solo con cabecera → `ZeroDivisionError` | División entre `len([])` sin comprobación | `promedio()` lanza `ValueError` claro; `main()` muestra `AVISO:` y sale con código 1 |
| P2. Ruta fija y dependiente del directorio | Ejecutar desde otra carpeta → `FileNotFoundError` | `ARCHIVO = 'ventas.csv'` en el código, relativo al directorio actual | `VENTAS_CSV` (relativa al proyecto o absoluta) con valor por defecto `ventas.csv` |
| P3. Entrada sin validar | `abc`, `10,5`, `nan`, `-10`, cabecera `venta`, CSV con BOM | `float(fila['ventas'])` sin controles; `open()` sin `encoding` | `carga.py` valida archivo, cabecera y cada fila; `encoding="utf-8-sig"` |
| P4. Código monolítico, sin pruebas ni entorno | No se puede probar el cálculo aislado | Lectura, cálculo e impresión en una función; factor `1.1` fijo | Paquete `src/demanda` (config, carga, cálculo, main); `FACTOR_DEMANDA`; pytest; `.venv` |

## Entorno

Python: **3.12.0** · intérprete VS Code: **`.venv\Scripts\python.exe`** (`.vscode/settings.json`) · comando de instalación: **`python -m pip install -r requirements.txt`**

- `.venv` creado con `py -3.12 -m venv .venv`; **no se versiona** (estaba subido por error y se retiró con `git rm -r --cached .venv`).
- `requirements.txt` con versiones fijas: `python-dotenv==1.2.4`, `pytest==9.2.0`, `ruff==0.17.4` y `-e .` (el propio paquete).
- Se eliminó `SQLAlchemy` de las dependencias: no se usa (la base de datos queda como mejora futura, observación 3).
- `.python-version` corregido de 3.14 a 3.12 (versión instalada y usada en el `.venv`).
- `.gitignore`: `.venv/`, `.env`, cachés (`__pycache__`, `.pytest_cache`, `.ruff_cache`), `*.egg-info`.
- Instalación desde cero comprobada en una carpeta limpia siguiendo solo el README: instala, ejecuta, `ruff check .` sin errores y `33 passed`.
- [ ] Captura de VS Code con el intérprete `.venv` seleccionado (barra de estado inferior) — **pendiente de hacer por la pareja**.

## Calidad

Resultado `ruff check .`: **All checks passed!** (`ruff format --check .`: 9 files already formatted) · decisión de modularización:

| Módulo | Responsabilidad |
|---|---|
| `calculo.py` | Lógica de negocio pura: `promedio`, `estimar`, `validar_factor`. No lee archivos ni imprime. |
| `carga.py` | Entrada: valida el archivo y cada fila del CSV; lanza `DatosInvalidosError` con el número de fila. |
| `config.py` | Configuración externa: `VENTAS_CSV`, `FACTOR_DEMANDA` y archivo `.env` (`python-dotenv`). |
| `main.py` | Interfaz: une las piezas, captura errores, muestra `AVISO:` y redondea a 2 decimales. |

## Pruebas

Casos implementados: **66 pruebas** en dos baterías.

**`test_app.py`** (Boris Castellanos Matamoros, 33 pruebas sobre `app.py`):

- **Normal:** `test_estimar_con_factor_por_defecto`, `test_estimar_con_factor_personalizado`, `test_cargar_ventas_correcto`, `test_main_correcto`.
- **Vacío:** `test_estimar_sin_ventas`, `test_cargar_ventas_solo_cabecera`, `test_validar_archivo_vacio`, `test_main_sin_ventas_muestra_aviso`.
- **Negativos:** `test_convertir_venta_invalida[-5-negativas]`.
- **Parámetro inválido:** `test_obtener_factor_invalido` (`abc`, `0`, `-1`, `inf`, `nan`).
- **Otros:** configuración por variables de entorno, validación del archivo (inexistente, carpeta, extensión, vacío), conversión de ventas, cabecera incorrecta, coma decimal, archivo inexistente en `main`.

**`tests/`** (33 pruebas por módulo del paquete `src/demanda`): cálculo, carga del CSV (incluye BOM de Excel, `nan`, celda vacía) y configuración (rutas relativa y absoluta).

Resultado `pytest -q`: **66 passed** (`python -m pytest test_app.py -q`: 33 passed)

## Transferencia

Otra pareja: ___ · ¿instaló sin ayuda?: ___ · incidencias y cambios: ___

| Incidencia | Causa | Corrección |
|---|---|---|
| _(rellenar tras la prueba)_ | | |

## Colaboración

Enlace repositorio/PR: https://github.com/adobrasca512/PROGRAMACION-Y-ENTORNOS-DE-TRABAJO-MISION-07 · rama `feature/profesionalizar` · PR: ___
Commits de cada integrante: ___

## Uso de IA

Herramienta: Claude Code (asistente de IA en VS Code). Finalidad: reproducir los fallos del proyecto heredado, proponer la refactorización en `src/`, redactar pruebas, README y documentación, y generar capturas del código y de la terminal. Fragmentos revisados y comprobaciones propias: ___ (indicar qué revisó cada integrante y cómo lo comprobó, p. ej. ejecutando `pytest -q` y modificando un caso).
