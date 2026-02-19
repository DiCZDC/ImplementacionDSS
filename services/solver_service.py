from model.goal_model import build_goal_model

def solve_model(data):

    model, variables = build_goal_model(data)

    model.solve()

    resultados = {
        "productos": [x.varValue for x in variables["X"]],
        "under_ganancia": variables["UNDER1"].varValue,
        "over_horas": variables["OVER2"].varValue,
        "over_presupuesto": variables["OVER3"].varValue
    }

    return resultados