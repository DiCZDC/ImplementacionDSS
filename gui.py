import tkinter as tk
from tkinter import ttk, messagebox
from services.solver_service import solve_model
from utils.output_formatter import show_results
from utils.pdf.generate_pdf import generate_pdf

class DSS_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DSS - Modelo MBI de Programación por Metas")
        self.root.geometry("800x550")
        
        # Variables
        self.num_productos = tk.IntVar(value=3)
        self.product_entries = []
        
        # Crear UI principal
        self.create_widgets()
        
    def create_widgets(self):
        """Crea la interfaz principal"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title = ttk.Label(main_frame, text="=== DSS Modelo MBI ===", 
                         font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=5)
        
        # Sección: Número de productos
        ttk.Label(main_frame, text="Número de productos:").grid(row=1, column=0, sticky=tk.W, pady=2)
        num_spinbox = ttk.Spinbox(main_frame, from_=1, to=20, textvariable=self.num_productos,
                                 command=self.update_products, width=10)
        num_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Frame para los productos (con scroll)
        canvas_frame = ttk.LabelFrame(main_frame, text="Datos de Productos", padding="5")
        canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        canvas = tk.Canvas(canvas_frame, height=120)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.products_frame = scrollable_frame
        self.products_canvas = canvas
        self.update_products()
        
        # Sección: Metas
        metas_frame = ttk.LabelFrame(main_frame, text="Metas", padding="5")
        metas_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(metas_frame, text="Meta de ganancia:").grid(row=0, column=0, sticky=tk.W, padx=3)
        self.meta_ganancia = ttk.Entry(metas_frame, width=12)
        self.meta_ganancia.insert(0, "5000000")
        self.meta_ganancia.grid(row=0, column=1, sticky=tk.W, padx=3)
        
        ttk.Label(metas_frame, text="Límite de horas:").grid(row=1, column=0, sticky=tk.W, padx=3)
        self.meta_horas = ttk.Entry(metas_frame, width=12)
        self.meta_horas.insert(0, "200000")
        self.meta_horas.grid(row=1, column=1, sticky=tk.W, padx=3)
        
        ttk.Label(metas_frame, text="Límite de presupuesto:").grid(row=2, column=0, sticky=tk.W, padx=3)
        self.meta_presupuesto = ttk.Entry(metas_frame, width=12)
        self.meta_presupuesto.insert(0, "8000000")
        self.meta_presupuesto.grid(row=2, column=1, sticky=tk.W, padx=3)
        
        # Sección: Pesos (Prioridades)
        pesos_frame = ttk.LabelFrame(main_frame, text="Pesos (Prioridad)", padding="5")
        pesos_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(pesos_frame, text="Peso ganancia no alcanzada:").grid(row=0, column=0, sticky=tk.W, padx=3)
        self.peso_ganancia = ttk.Entry(pesos_frame, width=12)
        self.peso_ganancia.insert(0, "1000")
        self.peso_ganancia.grid(row=0, column=1, sticky=tk.W, padx=3)
        
        ttk.Label(pesos_frame, text="Peso horas excedidas:").grid(row=1, column=0, sticky=tk.W, padx=3)
        self.peso_horas = ttk.Entry(pesos_frame, width=12)
        self.peso_horas.insert(0, "50")
        self.peso_horas.grid(row=1, column=1, sticky=tk.W, padx=3)
        
        ttk.Label(pesos_frame, text="Peso presupuesto excedido:").grid(row=2, column=0, sticky=tk.W, padx=3)
        self.peso_presupuesto = ttk.Entry(pesos_frame, width=12)
        self.peso_presupuesto.insert(0, "100")
        self.peso_presupuesto.grid(row=2, column=1, sticky=tk.W, padx=3)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=5)
        
        ttk.Button(buttons_frame, text="Resolver", command=self.solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Limpiar", command=self.clear).pack(side=tk.LEFT, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def update_products(self):
        """Actualiza el número de campos de productos"""
        # Limpiar frame anterior
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        self.product_entries = []
        num = self.num_productos.get()
        
        # Crear headers
        ttk.Label(self.products_frame, text="Producto", font=("Arial", 8, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=3, pady=2)
        ttk.Label(self.products_frame, text="Utilidad", font=("Arial", 8, "bold")).grid(
            row=0, column=1, sticky=tk.W, padx=3, pady=2)
        ttk.Label(self.products_frame, text="Costo", font=("Arial", 8, "bold")).grid(
            row=0, column=2, sticky=tk.W, padx=3, pady=2)
        ttk.Label(self.products_frame, text="Horas", font=("Arial", 8, "bold")).grid(
            row=0, column=3, sticky=tk.W, padx=3, pady=2)
        ttk.Label(self.products_frame, text="Mín.", font=("Arial", 8, "bold")).grid(
            row=0, column=4, sticky=tk.W, padx=3, pady=2)
        
        # Crear campos para cada producto
        for i in range(num):
            product_data = {}
            
            ttk.Label(self.products_frame, text=f"P{i+1}").grid(
                row=i+1, column=0, sticky=tk.W, padx=3, pady=2)
            
            product_data['utilidad'] = ttk.Entry(self.products_frame, width=10)
            product_data['utilidad'].grid(row=i+1, column=1, sticky=tk.W, padx=3, pady=2)
            product_data['utilidad'].insert(0, "1000")
            
            product_data['costo'] = ttk.Entry(self.products_frame, width=10)
            product_data['costo'].grid(row=i+1, column=2, sticky=tk.W, padx=3, pady=2)
            product_data['costo'].insert(0, "500")
            
            product_data['horas'] = ttk.Entry(self.products_frame, width=10)
            product_data['horas'].grid(row=i+1, column=3, sticky=tk.W, padx=3, pady=2)
            product_data['horas'].insert(0, "10")
            
            product_data['minimo'] = ttk.Entry(self.products_frame, width=8)
            product_data['minimo'].grid(row=i+1, column=4, sticky=tk.W, padx=3, pady=2)
            product_data['minimo'].insert(0, "0")
            
            self.product_entries.append(product_data)
    
    def solve(self):
        """Resuelve el modelo con los datos ingresados"""
        try:
            # Validar y recopilar datos
            data = {
                "n": self.num_productos.get(),
                "utilidades": [],
                "costos": [],
                "horas": [],
                "minimos": [],
                "meta_ganancia": float(self.meta_ganancia.get()),
                "meta_horas": float(self.meta_horas.get()),
                "meta_presupuesto": float(self.meta_presupuesto.get()),
                "peso_ganancia": float(self.peso_ganancia.get()),
                "peso_horas": float(self.peso_horas.get()),
                "peso_presupuesto": float(self.peso_presupuesto.get())
            }
            
            # Validar y recopilar datos de productos
            for i, product in enumerate(self.product_entries):
                try:
                    data["utilidades"].append(float(product['utilidad'].get()))
                    data["costos"].append(float(product['costo'].get()))
                    data["horas"].append(float(product['horas'].get()))
                    data["minimos"].append(float(product['minimo'].get()))
                except ValueError:
                    messagebox.showerror("Error", f"Valores inválidos en Producto {i+1}")
                    return
            
            # Resolver
            results = solve_model(data)
            
            # Mostrar resultados
            self.show_results_window(results)
            
        except ValueError as e:
            messagebox.showerror("Error de validación", f"Por favor ingrese valores válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver:\n{str(e)}")
    
    def show_results_window(self, results):
        generate_pdf(results)
        """Muestra una ventana con los resultados"""
        results_window = tk.Toplevel(self.root)
        results_window.title("Resultados")
        results_window.geometry("600x500")
        
        # Crear frame con scroll
        canvas = tk.Canvas(results_window)
        scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar resultados
        if results["status"] == "Optimal":
            status_text = f"Estado: ÓPTIMO (Valor objetivo: {results['objective']:.2f})"
            status_label = ttk.Label(scrollable_frame, text=status_text, 
                                    font=("Arial", 11, "bold"), foreground="green")
        else:
            status_text = f"Estado: {results['status']}"
            status_label = ttk.Label(scrollable_frame, text=status_text, 
                                    font=("Arial", 11, "bold"), foreground="red")
        
        status_label.pack(pady=10)
        
        # Cantidades producidas
        ttk.Label(scrollable_frame, text="Cantidades Producidas:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        for i, qty in enumerate(results.get("quantities", [])):
            if qty is not None:
                qty_text = f"Producto {i+1}: {qty:.2f} unidades"
                ttk.Label(scrollable_frame, text=qty_text).pack(anchor=tk.W, padx=20)
        
        # Desviaciones
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Desviaciones:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        for key, value in results.get("deviations", {}).items():
            if value is not None:
                dev_text = f"{key}: {value:.2f}"
                ttk.Label(scrollable_frame, text=dev_text).pack(anchor=tk.W, padx=20)
        
        # Limitaciones
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Análisis de Limitaciones:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        for limit, value in results.get("utilization", {}).items():
            limit_text = f"{limit}: {value}"
            ttk.Label(scrollable_frame, text=limit_text).pack(anchor=tk.W, padx=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón para cerrar
        ttk.Button(results_window, text="Cerrar", 
                  command=results_window.destroy).pack(pady=10)
    
    def clear(self):
        """Limpia todos los campos"""
        # Limpiar campos de productos
        for product in self.product_entries:
            for field in ['utilidad', 'costo', 'horas', 'minimo']:
                product[field].delete(0, tk.END)
        
        # Limpiar campos de metas
        self.meta_ganancia.delete(0, tk.END)
        self.meta_horas.delete(0, tk.END)
        self.meta_presupuesto.delete(0, tk.END)
        
        # Limpiar campos de pesos
        self.peso_ganancia.delete(0, tk.END)
        self.peso_horas.delete(0, tk.END)
        self.peso_presupuesto.delete(0, tk.END)


def main_gui():
    root = tk.Tk()
    app = DSS_GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main_gui()
