from model.goal_model import build_goal_model
import pulp

def solve_model(data):

    model, variables = build_goal_model(data)

    model.solve()
    
    # Obtener el estado del solver
    status = pulp.LpStatus[model.status]

    resultados = {
        "status": status,
        "objective": pulp.value(model.objective),
        "productos": [x.varValue for x in variables["X"]],
        "quantities": [x.varValue for x in variables["X"]],
        "under_ganancia": variables["UNDER1"].varValue,
        "over_horas": variables["OVER2"].varValue,
        "over_presupuesto": variables["OVER3"].varValue,
        "deviations": {
            "Ganancia no alcanzada": variables["UNDER1"].varValue,
            "Horas excedidas": variables["OVER2"].varValue,
            "Presupuesto excedido": variables["OVER3"].varValue
        },
        "utilization": {
            "Ganancia no alcanzada": f"{variables['UNDER1'].varValue:.2f}",
            "Horas excedidas": f"{variables['OVER2'].varValue:.2f}",
            "Presupuesto excedido": f"{variables['OVER3'].varValue:.2f}"
        }
    }

    return resultados