MAX_PRODUCTOS = 10
MIN_PRODUCTOS = 1

DEFAULTS_PRODUCTO = [
    {"utilidad": 8000,  "horas": 300, "costo": 10000, "minimo": 100},
    {"utilidad": 12000, "horas": 500, "costo": 15000, "minimo": 200},
]

DEFAULTS_METAS = {
    "ganancia":    5000000,
    "horas":       200000,
    "presupuesto": 8000000,
}

DEFAULTS_PESOS = {
    "over1":  0,
    "under1": 1000,
    "over2":  50,
    "under2": 10,
    "over3":  100,
    "under3": 20,
}

SOLVER_METHOD = "highs"
