from dataclasses import dataclass, field
from typing import List
from scipy.optimize import linprog
from config import SOLVER_METHOD
from model.goal_model import LinearProgram, ModelData


@dataclass
class DeviationRow:
    nombre:   str
    actual:   float
    objetivo: float

    @property
    def desviacion(self):
        return self.actual - self.objetivo

    @property
    def estado(self):
        if abs(self.desviacion) < 1:
            return "en_meta"
        return "sobre" if self.desviacion > 0 else "bajo"


@dataclass
class SolverResult:
    exitoso:  bool
    mensaje:  str
    Z:        float = 0.0
    X:        List[float] = field(default_factory=list)
    over1:  float = 0.0
    under1: float = 0.0
    over2:  float = 0.0
    under2: float = 0.0
    over3:  float = 0.0
    under3: float = 0.0
    desviaciones: List[DeviationRow] = field(default_factory=list)


def solve(lp: LinearProgram, data: ModelData) -> SolverResult:
    raw = linprog(
        lp.c,
        A_ub=lp.A_ub or None,
        b_ub=lp.b_ub or None,
        A_eq=lp.A_eq,
        b_eq=lp.b_eq,
        bounds=lp.bounds,
        method=SOLVER_METHOD,
    )

    if raw.status != 0:
        return SolverResult(exitoso=False, mensaje=raw.message)

    x   = raw.x
    idx = lp.idx
    n   = data.n

    gain_real = sum(data.utilidades[i] * x[i] for i in range(n))
    hora_real = sum(data.horas[i]      * x[i] for i in range(n))
    pres_real = sum(data.costos[i]     * x[i] for i in range(n))

    return SolverResult(
        exitoso=True,
        mensaje=raw.message,
        Z=raw.fun,
        X=[x[i] for i in range(n)],
        over1=x[idx["O1"]],  under1=x[idx["U1"]],
        over2=x[idx["O2"]],  under2=x[idx["U2"]],
        over3=x[idx["O3"]],  under3=x[idx["U3"]],
        desviaciones=[
            DeviationRow("Ganancia ($)",    gain_real, data.meta_ganancia),
            DeviationRow("Horas (hrs)",     hora_real, data.meta_horas),
            DeviationRow("Presupuesto ($)", pres_real, data.meta_presupuesto),
        ],
    )
