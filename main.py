import sys
import time
import os

from utils.colors import C
from utils.input_handler import recopilar_datos, clear, header
from utils.output_formatter import mostrar_resultado, mostrar_resumen
from model.goal_model import build
from services.solver_service import solve


def seleccionar_modo():
    clear()
    print(f"\n{C.CYAN}{C.BOLD}  PROGRAMACION POR METAS MBI - SOFTWARE{C.RESET}")
    print(f"  {'─' * 30}\n")
    print(f"  Como quieres usar el programa?\n")
    print(f"  {C.BOLD}1{C.RESET}  Interfaz grafica (GUI)")
    print(f"  {C.BOLD}2{C.RESET}  Terminal (CLI)")
    print(f"  {C.BOLD}0{C.RESET}  Salir\n")
    while True:
        op = input("  Opcion: ").strip()
        if op in ("0", "1", "2"):
            return op
        print(f"  {C.RED}Ingresa 0, 1 o 2.{C.RESET}")


def run_gui():
    try:
        from gui.app import launch
        launch()
    except ImportError:
        print(f"\n  {C.RED}No se pudo iniciar la GUI.{C.RESET}")
        print("  En Windows tkinter ya viene con Python.")
        print("  En Linux instala con: sudo apt install python3-tk\n")
        input("  Enter para continuar en modo CLI...")
        run_cli()


def _pausa():
    input(f"\n  Presiona Enter para continuar...")


def run_cli():
    data = None

    while True:
        clear()
        header()
        print(f"  {C.BOLD}Menu principal{C.RESET}\n")
        print(f"  1  Ingresar datos y resolver")
        if data:
            print(f"  2  Ver resumen del modelo")
            print(f"  3  Resolver de nuevo")
        print(f"  0  Salir\n")
        op = input("  Opcion: ").strip()

        if op == "0":
            print("\n  Hasta luego.\n")
            sys.exit(0)
        elif op == "1":
            data   = recopilar_datos()
            result = solve(build(data), data)
            clear()
            header()
            mostrar_resultado(result, data)
            _pausa()
        elif op == "2" and data:
            clear()
            header()
            mostrar_resumen(data)
            _pausa()
        elif op == "3" and data:
            result = solve(build(data), data)
            clear()
            header()
            mostrar_resultado(result, data)
            _pausa()
        else:
            print(f"  {C.RED}Opcion no valida.{C.RESET}")
            time.sleep(1)


def main():
    op = seleccionar_modo()
    if op == "0":
        sys.exit(0)
    elif op == "1":
        run_gui()
    elif op == "2":
        run_cli()


if __name__ == "__main__":
    main()
