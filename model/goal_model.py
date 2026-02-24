from dataclasses import dataclass, field
from typing import List


@dataclass
class ModelData:
    n: int
    utilidades:  List[float]
    horas:       List[float]
    costos:      List[float]
    minimos:     List[float]
    meta_ganancia:    float
    meta_horas:       float
    meta_presupuesto: float
    peso_over1:  float
    peso_under1: float
    peso_over2:  float
    peso_under2: float
    peso_over3:  float
    peso_under3: float


@dataclass
class LinearProgram:
    c:      List[float]
    A_ub:   List[List[float]]
    b_ub:   List[float]
    A_eq:   List[List[float]]
    b_eq:   List[float]
    bounds: List[tuple]
    idx:    dict = field(default_factory=dict)


def build(data: ModelData) -> LinearProgram:
    n = data.n
    total = n + 6

    idx = {
        "O1": n,   "U1": n+1,
        "O2": n+2, "U2": n+3,
        "O3": n+4, "U3": n+5,
    }

    c = [0.0] * total
    c[idx["O1"]] = data.peso_over1
    c[idx["U1"]] = data.peso_under1
    c[idx["O2"]] = data.peso_over2
    c[idx["U2"]] = data.peso_under2
    c[idx["O3"]] = data.peso_over3
    c[idx["U3"]] = data.peso_under3

    A_eq, b_eq = [], []

    def meta_row(coefs, oi, ui):
        row = [0.0] * total
        for i, v in enumerate(coefs):
            row[i] = v
        row[oi] = -1.0
        row[ui] =  1.0
        return row

    A_eq.append(meta_row(data.utilidades, idx["O1"], idx["U1"]))
    b_eq.append(data.meta_ganancia)
    A_eq.append(meta_row(data.horas, idx["O2"], idx["U2"]))
    b_eq.append(data.meta_horas)
    A_eq.append(meta_row(data.costos, idx["O3"], idx["U3"]))
    b_eq.append(data.meta_presupuesto)

    A_ub, b_ub = [], []
    for i in range(n):
        row = [0.0] * total
        row[i] = -1.0
        A_ub.append(row)
        b_ub.append(-data.minimos[i])

    bounds = [(0.0, None)] * total

    return LinearProgram(c=c, A_ub=A_ub, b_ub=b_ub,
                         A_eq=A_eq, b_eq=b_eq,
                         bounds=bounds, idx=idx)
