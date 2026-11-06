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

```powershell
python -m pytest
```
