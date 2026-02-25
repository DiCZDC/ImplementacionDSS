# DSS — Goal Programming MBI

Sistema de Soporte de Decisiones basado en **Programación por Metas** Goal Programming método MBI.  
Permite ingresar productos, metas y pesos de penalización de forma interactiva y resuelve el modelo de optimización lineal.

---

## Estructura del proyecto

```
ImplementacionDSS/
├── gui/
│   ├── __init__.py
│   └── app.py 
├── model/
│   ├── __init__.py
│   └── goal_model.py        
├── services/
│   ├── __init__.py
│   └── solver_service.py   
├── utils/
│   ├── __init__.py
│   ├── colors.py           
│   ├── input_handler.py     
│   └── output_formatter.py  
├── config.py                
├── main.py                 
├── requirements.txt
└── .gitignore
```
El programa se encuentra dividido en 3 secciones principales, además de archivos de configuración y ejecución:

    utils/
        input_handler.py: solicita por consola los datos del problema (productos, utilidades, costos, horas, metas y pesos) y los devuelve en un diccionario.
        output_formatter.py: devuelve la producción recomendada y el cumplimiento de metas (ganancia, horas y presupuesto).

    services/
        solver_service.py: conecta el modelo con el "solver"

    model/
        goal_model.py: define el Modelo de Programación por Metas (MBI)

    main.py
        Punto de inicio de la ejecución del programa

    config.py
        Contiene los valores de ejemplo

    requirements.txt
        Lista de dependencias del proyecto.

    .gitignore
        Define archivos/carpetas que Git no debe versionar (por ejemplo, entornos virtuales y cachés).

## Instalación

```
# 1. Clona o descarga el proyecto
cd ImplementacionDSS

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Ejecutar
python main.py

```