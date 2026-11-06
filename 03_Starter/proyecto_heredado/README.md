# Previsión de demanda

Calcula la **demanda prevista** de un producto a partir de su histórico de ventas:
`demanda = promedio de ventas × factor de ajuste` (factor 1.1 por defecto).

Autores: Adilem Dobras Castillo · Boris Castellanos Matamoros

## Requisitos

- **Python 3.12** (comprobado con 3.12.0; ver `.python-version`)
- Git
- VS Code con las extensiones **Python** y **Ruff** (VS Code las sugiere al abrir la carpeta)

## Instalación desde cero

Todos los comandos se ejecutan **dentro de la carpeta del proyecto** (la que contiene este README).

### Windows (PowerShell)

```powershell
git clone https://github.com/adobrasca512/PROGRAMACION-Y-ENTORNOS-DE-TRABAJO-MISION-07.git
cd "PROGRAMACION-Y-ENTORNOS-DE-TRABAJO-MISION-07\03_Starter\proyecto_heredado"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repetir el `Activate.ps1`.

### macOS / Linux

```bash
git clone https://github.com/adobrasca512/PROGRAMACION-Y-ENTORNOS-DE-TRABAJO-MISION-07.git
cd PROGRAMACION-Y-ENTORNOS-DE-TRABAJO-MISION-07/03_Starter/proyecto_heredado
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

`requirements.txt` instala las dependencias con versión fija y el propio proyecto en modo editable (`-e .`).

### Comprobar el entorno

```powershell
python --version                 # Python 3.12.x
python -c "import sys; print(sys.executable)"   # debe apuntar a ...\.venv\...
python -m pip list
```

En VS Code: abrir **esta carpeta** (`File → Open Folder`), `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`. El archivo `.vscode/settings.json` ya apunta a ese intérprete.

## Configuración

Se configura con variables de entorno o con el archivo `.env` (copiado de `.env.example`; **no se sube a Git**):

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `VENTAS_CSV` | `data/ventas.csv` | Ruta del CSV. Relativa a la carpeta del proyecto o absoluta. |
| `FACTOR_DEMANDA` | `1.1` | Factor de ajuste. Número mayor que 0. |

Las variables definidas en la terminal tienen prioridad sobre el `.env`:

```powershell
$env:FACTOR_DEMANDA = "1.25"; python -m demanda      # Windows
FACTOR_DEMANDA=1.25 python -m demanda                 # macOS / Linux
```

### Formato del CSV

Codificación UTF-8 (también acepta el UTF-8 con BOM que guarda Excel), una columna `ventas` con números enteros no negativos:

```csv
ventas
10
20
30
```

## Ejecución

```powershell
python -m demanda          # o bien: prevision-demanda
```

Salida esperada con `data/ventas.csv`:

```text
Ventas leídas: 3
Promedio de ventas: 20.00
Demanda prevista: 22.00 (promedio x factor 1.10)
```

Si los datos o la configuración no son válidos, el programa muestra `AVISO: <motivo>` (por ejemplo `AVISO: Fila 3: 'abc' no es un número.`) y termina con código 1, sin traza de error.

## Calidad y pruebas

```powershell
ruff check .
ruff format --check .
python -m pytest -q
```

## Estructura

```text
proyecto_heredado/
├── src/demanda/
│   ├── calculo.py     # lógica de negocio: promedio, estimar, validar_factor
│   ├── carga.py       # entrada: lectura y validación del CSV
│   ├── config.py      # configuración: variables de entorno y .env
│   ├── main.py        # interfaz de consola
│   └── __main__.py    # permite `python -m demanda`
├── tests/             # pruebas pytest
├── data/ventas.csv    # datos de ejemplo
├── .env.example       # plantilla de configuración
├── .vscode/           # intérprete y extensiones recomendadas
├── pyproject.toml     # paquete, pytest y Ruff
├── requirements.txt
├── diagnostico.md     # reto 1: problemas del proyecto heredado
└── evidencias.md      # evidencias de la misión
```

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `No module named demanda` | Activar `.venv` y ejecutar `python -m pip install -r requirements.txt`. |
| `Activate.ps1 no se puede cargar` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. |
| `AVISO: No se encontró el archivo de ventas` | Revisar `VENTAS_CSV` en `.env` o en la terminal. |
| VS Code no reconoce los imports | Seleccionar el intérprete `.venv` (ver *Comprobar el entorno*). |
