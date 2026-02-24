import os
from utils.colors import C
from config import MAX_PRODUCTOS, MIN_PRODUCTOS, DEFAULTS_PRODUCTO, DEFAULTS_METAS, DEFAULTS_PESOS
from model.goal_model import ModelData


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print(f"\n{C.CYAN}{C.BOLD}  DSS - Goal Programming MBI{C.RESET}\n")

def section(t):
    print(f"\n{C.YELLOW}{C.BOLD}  {t}{C.RESET}")
    print(f"  {'─' * 40}")

def _err(msg):
    print(f"  {C.RED}Error: {msg}{C.RESET}")


def pedir_float(prompt, default=None, min_val=None):
    while True:
        suf = f" [{default}]" if default is not None else ""
        raw = input(f"  {prompt}{suf}: ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                _err(f"Debe ser >= {min_val}")
                continue
            return val
        except ValueError:
            _err("Ingresa un numero valido.")


def pedir_int(prompt, default=None, min_val=MIN_PRODUCTOS, max_val=MAX_PRODUCTOS):
    while True:
        suf = f" [{default}]" if default is not None else ""
        raw = input(f"  {prompt}{suf}: ").strip()
        if raw == "" and default is not None:
            return int(default)
        try:
            val = int(raw)
            if not (min_val <= val <= max_val):
                _err(f"Debe estar entre {min_val} y {max_val}.")
                continue
            return val
        except ValueError:
            _err("Ingresa un numero entero.")


def recopilar_datos():
    clear()
    header()

    section("Numero de productos")
    n = pedir_int(f"Cuantos productos? ({MIN_PRODUCTOS}-{MAX_PRODUCTOS})", default=2)

    section("Datos por producto")
    utilidades, horas, costos, minimos = [], [], [], []

    for i in range(n):
        d = DEFAULTS_PRODUCTO[i] if i < len(DEFAULTS_PRODUCTO) else {"utilidad": 0, "horas": 0, "costo": 0, "minimo": 0}
        print(f"\n  -- Producto {i+1} (X{i+1})")
        utilidades.append(pedir_float("  Utilidad por unidad ($)", default=d["utilidad"], min_val=0))
        horas.append(pedir_float("  Horas por unidad", default=d["horas"], min_val=0))
        costos.append(pedir_float("  Costo por unidad ($)", default=d["costo"], min_val=0))
        minimos.append(pedir_float("  Produccion minima", default=d["minimo"], min_val=0))

    section("Metas objetivo")
    d = DEFAULTS_METAS
    meta_g = pedir_float("Meta de Ganancia ($)", default=d["ganancia"], min_val=0)
    meta_h = pedir_float("Meta de Horas (hrs)", default=d["horas"], min_val=0)
    meta_p = pedir_float("Meta de Presupuesto ($)", default=d["presupuesto"], min_val=0)

    section("Pesos de penalizacion")
    print("  (0 = no penaliza esa desviacion)\n")
    d = DEFAULTS_PESOS
    print("  Ganancia:")
    o1 = pedir_float("  Peso OVER1  (superar meta)", default=d["over1"], min_val=0)
    u1 = pedir_float("  Peso UNDER1 (no alcanzar meta)", default=d["under1"], min_val=0)
    print("  Horas:")
    o2 = pedir_float("  Peso OVER2  (exceder horas)", default=d["over2"], min_val=0)
    u2 = pedir_float("  Peso UNDER2 (quedar corto)", default=d["under2"], min_val=0)
    print("  Presupuesto:")
    o3 = pedir_float("  Peso OVER3  (exceder presupuesto)", default=d["over3"], min_val=0)
    u3 = pedir_float("  Peso UNDER3 (quedar corto)", default=d["under3"], min_val=0)

    return ModelData(
        n=n,
        utilidades=utilidades, horas=horas, costos=costos, minimos=minimos,
        meta_ganancia=meta_g, meta_horas=meta_h, meta_presupuesto=meta_p,
        peso_over1=o1, peso_under1=u1,
        peso_over2=o2, peso_under2=u2,
        peso_over3=o3, peso_under3=u3,
    )
