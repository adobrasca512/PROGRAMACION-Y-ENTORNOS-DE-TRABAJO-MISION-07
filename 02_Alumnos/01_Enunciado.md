# MISIÓN 7 · El proyecto heredado
**Programación y Entornos en IA — Universidad Europea · 4 horas**

## Encargo profesional
Una consultora entrega un pequeño sistema que estima la demanda de un producto a partir de sus ventas recientes. Funciona en el ordenador del autor, pero está desorganizado, no tiene pruebas, mezcla configuración y lógica y no se puede reproducir con seguridad. En parejas, debéis convertirlo en un proyecto profesional.

**No se evalúa crear un modelo de IA complejo**: se evalúa el entorno, la calidad y la capacidad de reproducir y verificar un proyecto Python.

## Retos y evidencias
1. **Diagnóstico y rescate (40 min):** ejecutar el proyecto heredado, identificar al menos cuatro problemas y registrar los fallos iniciales. Evidencia: `diagnostico.md` con síntomas, causa y corrección propuesta.
2. **Entorno reproducible (45 min):** crear `.venv`, configurar VS Code, definir `requirements.txt` y `.gitignore`, documentar instalación desde cero. Evidencia: captura del intérprete activo, `python -m pip list` y comandos en README.
3. **Refactorización y calidad (50 min):** separar entrada/salida de lógica de negocio; añadir validaciones y configuración con variables de entorno; pasar Ruff. Evidencia: código modular, comprobación `ruff check .`.
4. **Pruebas y transferencia (50 min):** crear al menos cuatro pruebas pytest (normal, vacío, negativos, parámetro inválido), comprobar `pytest -q` y entregar a otra pareja para instalar sin instrucciones verbales. Evidencia: resultados, incidencias de transferencia y correcciones.
5. **Defensa individual (35 min):** cada integrante explica decisiones y resuelve una modificación sencilla en directo. Cada persona debe poder explicar el trabajo completo.

## Entrega
Repositorio Git con `src/`, `tests/`, `requirements.txt`, `.gitignore`, `README.md`, `diagnostico.md` y `evidencias.md`; enlace a rama o pull request, historial de commits y captura de pruebas. No subir `.venv`, secretos ni archivos temporales.

## Condiciones
Trabajo por parejas, defensa individual; se permite consultar documentación y usar herramientas de asistencia **solo si se declara el uso y se entiende el código**. La prueba de transferencia se hace sin ayuda oral del equipo autor. No es necesario Docker, AWS ni CI/CD.
