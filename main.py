from utils.input_handler import get_user_input
from services.solver_service import solve_model
from utils.output_formatter import show_results
from utils.pdf.generate_pdf import generate_pdf

def main():
    print("=== DSS Modelo MBI de programación por metas ===\n")
    
    data = get_user_input()
    results = solve_model(data)
    show_results(results)
    generate_pdf(results)

if __name__ == "__main__":
    main()