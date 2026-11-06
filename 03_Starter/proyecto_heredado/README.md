# Previsión de demanda

Calcula la demanda prevista a partir de un histórico de ventas.

## Requisitos

- Python 3.14
- VS Code con la extensión Python

## Instalación

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Después edita `.env` con tus datos de conexión.

## Verificación

```powershell
python --version
python -m pip list
```

En VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`.

## Ejecución

```powershell
python app.py
```

## Tests

Los tests están en `test_app.py` y usan CSV temporales, así que no modifican `ventas.csv`.

Desde la carpeta del proyecto, con el entorno virtual activado (el prompt debe empezar por `(.venv)`):

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```

Resultado esperado: `33 passed`.

Otras opciones útiles:

```powershell
python -m pytest -q                          # salida resumida
python -m pytest test_app.py -k estimar      # solo los tests cuyo nombre contiene "estimar"
python -m ruff check .                       # revisión de estilo del código
```

Si PowerShell bloquea la activación del entorno, permite los scripts solo en esa ventana:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
