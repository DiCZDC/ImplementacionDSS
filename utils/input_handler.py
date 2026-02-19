def get_user_input():
    print("=== CONFIGURACIÓN DEL DSS ===\n")

    n = int(input("¿Cuántos productos desea analizar?: "))

    utilidades = []
    costos = []
    horas = []

    for i in range(n):
        print(f"\nProducto {i+1}")
        utilidades.append(float(input("Utilidad por unidad: ")))
        costos.append(float(input("Costo por unidad: ")))
        horas.append(float(input("Horas requeridas por unidad: ")))

    print("\n--- Metas ---")
    meta_ganancia = float(input("Meta de ganancia: "))
    meta_horas = float(input("Límite de horas disponibles: "))
    meta_presupuesto = float(input("Límite de presupuesto: "))

    print("\n--- Pesos (prioridad) ---")
    peso_ganancia = float(input("Peso para NO alcanzar ganancia: "))
    peso_horas = float(input("Peso para EXCEDER horas: "))
    peso_presupuesto = float(input("Peso para EXCEDER presupuesto: "))

    return {
        "n": n,
        "utilidades": utilidades,
        "costos": costos,
        "horas": horas,
        "meta_ganancia": meta_ganancia,
        "meta_horas": meta_horas,
        "meta_presupuesto": meta_presupuesto,
        "peso_ganancia": peso_ganancia,
        "peso_horas": peso_horas,
        "peso_presupuesto": peso_presupuesto
    }