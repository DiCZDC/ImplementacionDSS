from utils.colors import C
from model.goal_model import ModelData
from services.solver_service import SolverResult


def section(t):
    print(f"\n{C.YELLOW}{C.BOLD}  {t}{C.RESET}")
    print(f"  {'─' * 40}")


def mostrar_resultado(result: SolverResult, data: ModelData):
    section("Resultado")

    if not result.exitoso:
        print(f"  {C.RED}Sin solucion: {result.mensaje}{C.RESET}")
        return

    print(f"\n  {C.GREEN}Solucion optima encontrada{C.RESET}")
    print(f"  Z = {C.CYAN}{result.Z:,.2f}{C.RESET}\n")

    section("Variables de decision")
    for i, val in enumerate(result.X):
        print(f"  X{i+1} = {C.CYAN}{val:,.2f}{C.RESET}  (min: {data.minimos[i]:,.0f})")

    section("Variables de desviacion")
    devs = [
        ("OVER1",  result.over1,  "Ganancia supera meta"),
        ("UNDER1", result.under1, "Ganancia bajo meta"),
        ("OVER2",  result.over2,  "Horas exceden meta"),
        ("UNDER2", result.under2, "Horas quedan cortas"),
        ("OVER3",  result.over3,  "Presupuesto excede meta"),
        ("UNDER3", result.under3, "Presupuesto queda corto"),
    ]
    for nombre, val, desc in devs:
        if val < 0.01:
            color = C.DIM
        elif "OVER" in nombre:
            color = C.YELLOW
        else:
            color = C.RED
        print(f"  {nombre:<8} = {color}{val:,.2f}{C.RESET}  ({desc})")

    section("Analisis de metas")
    print(f"\n  {'Meta':<20} {'Alcanzado':>12} {'Objetivo':>12} {'Desviacion':>12}  Estado")
    print(f"  {'─'*20} {'─'*12} {'─'*12} {'─'*12}  {'─'*16}")

    estados = {"en_meta": (C.GREEN, "En meta"), "sobre": (C.YELLOW, "Sobre la meta"), "bajo": (C.RED, "Bajo la meta")}
    for row in result.desviaciones:
        color, label = estados[row.estado]
        dev_str = f"{'+' if row.desviacion >= 0 else ''}{row.desviacion:,.0f}"
        print(f"  {row.nombre:<20} {row.actual:>12,.0f} {row.objetivo:>12,.0f} {dev_str:>12}  {color}{label}{C.RESET}")

    print()


def mostrar_resumen(data: ModelData):
    section("Resumen del modelo")
    print(f"\n  Productos: {data.n}")
    print(f"\n  {'Producto':<10} {'Utilidad':>12} {'Horas':>8} {'Costo':>12} {'Minimo':>8}")
    print(f"  {'─'*10} {'─'*12} {'─'*8} {'─'*12} {'─'*8}")
    for i in range(data.n):
        print(f"  {'X'+str(i+1):<10} {data.utilidades[i]:>12,.0f} {data.horas[i]:>8,.0f} {data.costos[i]:>12,.0f} {data.minimos[i]:>8,.0f}")

    print(f"\n  Metas:")
    print(f"    Ganancia:    {data.meta_ganancia:>15,.0f}")
    print(f"    Horas:       {data.meta_horas:>15,.0f}")
    print(f"    Presupuesto: {data.meta_presupuesto:>15,.0f}")

    print(f"\n  Pesos:")
    print(f"    OVER1={data.peso_over1}  UNDER1={data.peso_under1}  OVER2={data.peso_over2}  UNDER2={data.peso_under2}  OVER3={data.peso_over3}  UNDER3={data.peso_under3}")
    print()
