# ImplementacionDSS: 'DSS - Programación por Metas (Modelo MBI)'

## Descripción:
Este sistema implementa un modelo de Programación por Metas utilizando el enfoque MBI.
Permite al usuario ingresar metas y prioridades, y genera una recomendación óptima
minimizando las desviaciones ponderadas.

## Ejecución:
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar:
   ```bash
   python main.py
   ```

## Estructura del proyecto
```text
ImplementacionDSS/
├─ model/
│  └─ goal_model.py
├─ services/
│  └─ solver_service.py
├─ utils/
│  ├─ input_handler.py
│  └─ output_formatter.py
├─ .gitignore
├─ README.md
├─ config.py
├─ main.py
├─ requirements.txt
```
El programa se encuentra dividido en 3 secciones principales, además de archivos de configuración y ejecución:

- utils/
   - input_handler.py: solicita por consola los datos del problema (productos, utilidades, costos, horas, metas y pesos) y los devuelve en un diccionario.
   - output_formatter.py: devuelve la producción recomendada y el cumplimiento de metas (ganancia, horas y presupuesto).

- services/
   - solver_service.py: conecta el modelo con el "solver"

- model/
   - goal_model.py: define el **Modelo de Programación por Metas** (MBI)

- main.py
   - Punto de inicio de la ejecución del programa

- config.py
   - Contiene los valores por defecto de metas y pesos (actualmente declarados como constantes)

- requirements.txt
   - Lista de dependencias del proyecto.

- .gitignore
   - Define archivos/carpetas que Git no debe versionar (por ejemplo, entornos virtuales y cachés).
