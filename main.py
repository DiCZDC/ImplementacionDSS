from utils.input_handler import get_user_input
from services.solver_service import solve_model
from utils.output_formatter import show_results
from gui import main_gui
import sys
from utils.pdf.generate_pdf import generate_pdf

def main():
    print("=== DSS Modelo MBI de programación por metas ===\n")
    print("Seleccione modalidad:")
    print("1. Interfaz gráfica (GUI)")
    print("2. Línea de comandos")
    
    opcion = input("\nIngrese su opción (1 o 2): ").strip()
    
    if opcion == "1":
        main_gui()
    elif opcion == "2":
        data = get_user_input()
        results = solve_model(data)
        show_results(results)
    else:
        print("Opción inválida. Por favor ingrese 1 o 2.")
        main()

if __name__ == "__main__":
    # Si se pasa argumento GUI, abre directamente la interfaz gráfica
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        main_gui()
    else:
        main()