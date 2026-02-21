from fpdf import FPDF
from pathlib import Path

def generate_pdf(results):
    pdf = FPDF()
    pdf.set_font("helvetica", size=20)

    # Cabecera con iconos:
    pdf.add_page()
    pdf.image(
        str(Path(__file__).resolve().parent / "images" / "tecnm.png"), 10, 0, 50, 0, ""
    )
    pdf.image(
        str(Path(__file__).resolve().parent / "images" / "ito.png"),160,10,30,0,""
    )

    #Titulo
    pdf.set_top_margin(60)
    pdf.set_font_size(20)
    pdf.cell(0, 60, f"RECOMENDACIONES DSS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font_size(18)
    pdf.set_y(pdf.get_y()-20)
    pdf.cell(0, 0, f"Proyecto Equipo 5", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(pdf.get_y()+15)
    #Producción recomendada
    pdf.set_font_size(16)
    pdf.cell(0, 10, "1. Producción recomendada", align="L", new_x="LMARGIN", new_y="NEXT")
    for i, cantidad in enumerate(results["productos"]):
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.cell(10, 10, f"{i+1}. Producto {i+1}:       {cantidad}", align="L", new_x="LMARGIN", new_y="NEXT")
    # Evaluación de metas
    pdf.cell(0, 10, "2. Evaluación de metas", align="L", new_x="LMARGIN", new_y="NEXT")
    if results["under_ganancia"] > 0:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.cell(10, 10, f"No se alcanzó la meta de ganancia por: {results['under_ganancia']}", align="L", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(10, 10, "Meta de ganancia alcanzada o superada.", align="L", new_x="LMARGIN", new_y="NEXT")

    # Evaluación de horas
    pdf.cell(0, 10, "3. Evaluación de horas", align="L", new_x="LMARGIN", new_y="NEXT")
    if results["over_horas"] > 0:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.cell(10, 10, f"Exceso de horas: {results['over_horas']}", align="L", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(10, 10, "Horas dentro del límite.", align="L", new_x="LMARGIN", new_y="NEXT")

    # Evaluación de presupuesto
    pdf.cell(0, 10, "4. Evaluación de presupuesto", align="L", new_x="LMARGIN", new_y="NEXT")
    if results["over_presupuesto"] > 0:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.cell(10, 10, f"Exceso de presupuesto: {results['over_presupuesto']}", align="L", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font_size(14)
        pdf.set_x(20)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(10, 10, "Presupuesto dentro del límite.", align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.output("Recomendaciones.pdf")
