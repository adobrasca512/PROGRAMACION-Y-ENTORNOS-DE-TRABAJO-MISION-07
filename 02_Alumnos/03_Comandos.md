# Chuleta de comandos
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest -q
ruff check .
ruff format --check .
git status
git switch -c feature/profesionalizar
```
En VS Code: `Python: Select Interpreter` → `.venv`.
**Nunca subas `.venv/` ni `.env` a Git.**
