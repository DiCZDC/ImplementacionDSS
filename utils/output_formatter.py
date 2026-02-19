def show_results(results):

    print("\n=== RESULTADOS DEL DSS ===\n")

    print("Producción recomendada:")
    for i, cantidad in enumerate(results["productos"]):
        print(f"Producto {i+1}: {cantidad}")

    print("\nEvaluación de metas:")

    if results["under_ganancia"] > 0:
        print(f"No se alcanzó la meta de ganancia por: {results['under_ganancia']}")
    else:
        print("Meta de ganancia alcanzada o superada.")

    if results["over_horas"] > 0:
        print(f"Exceso de horas: {results['over_horas']}")
    else:
        print("Horas dentro del límite.")

    if results["over_presupuesto"] > 0:
        print(f"Exceso de presupuesto: {results['over_presupuesto']}")
    else:
        print("Presupuesto dentro del límite.")