import pulp
from pulp import *

def build_goal_model(data):

    model = LpProblem("DSS_Goal_Programming", LpMinimize)

    n = data["n"]

    #variables de decisión dinámicas
    X = [LpVariable(f"Producto_{i+1}", lowBound=0) for i in range(n)]

    #variables de desviación
    OVER1 = LpVariable("Over_Ganancia", lowBound=0)
    UNDER1 = LpVariable("Under_Ganancia", lowBound=0)

    OVER2 = LpVariable("Over_Horas", lowBound=0)
    UNDER2 = LpVariable("Under_Horas", lowBound=0)

    OVER3 = LpVariable("Over_Presupuesto", lowBound=0)
    UNDER3 = LpVariable("Under_Presupuesto", lowBound=0)

   
    #ECUACIONES MBI GENERALES

    #meta  de ganancia
    model += (
        lpSum(data["utilidades"][i] * X[i] for i in range(n))
        - OVER1 + UNDER1
        == data["meta_ganancia"]
    )

    #meta de horas
    model += (
        lpSum(data["horas"][i] * X[i] for i in range(n))
        - OVER2 + UNDER2
        == data["meta_horas"]
    )

    #meta de presupuesto
    model += (
        lpSum(data["costos"][i] * X[i] for i in range(n))
        - OVER3 + UNDER3
        == data["meta_presupuesto"]
    )

    # FUNCIÓN OBJETIVO minimizar Z
    model += (
        data["peso_ganancia"] * UNDER1 +
        data["peso_horas"] * OVER2 +
        data["peso_presupuesto"] * OVER3
    )

    variables = {
        "X": X,
        "UNDER1": UNDER1,
        "OVER2": OVER2,
        "OVER3": OVER3
    }

    return model, variables