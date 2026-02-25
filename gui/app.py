import tkinter as tk
from tkinter import ttk, messagebox

from config import MAX_PRODUCTOS, MIN_PRODUCTOS, DEFAULTS_PRODUCTO, DEFAULTS_METAS, DEFAULTS_PESOS
from model.goal_model import ModelData, build
from services.solver_service import solve

BG     = "#f5f5f5"
WHITE  = "#ffffff"
DARK   = "#1a1a2e"
BLUE   = "#2563eb"
GREEN  = "#16a34a"
RED    = "#dc2626"
YELLOW = "#ca8a04"
GRAY   = "#6b7280"
BORDER = "#d1d5db"

FNT       = ("Segoe UI", 10)
FNT_B     = ("Segoe UI", 10, "bold")
FNT_TITLE = ("Segoe UI", 14, "bold")
FNT_SMALL = ("Segoe UI", 9)
FNT_BIG   = ("Segoe UI", 20, "bold")


def entry(parent, var, w=15):
    e = tk.Entry(parent, textvariable=var, width=w, font=FNT,
                 bg=WHITE, relief="solid", bd=1)
    return e

def lbl(parent, text, bold=False, color=DARK, size=10, **kw):
    f = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
    return tk.Label(parent, text=text, font=f, fg=color, bg=parent["bg"], **kw)

def btn(parent, text, cmd, color=BLUE, w=14):
    return tk.Button(parent, text=text, command=cmd,
                     bg=color, fg=WHITE, font=FNT_B,
                     relief="flat", cursor="hand2",
                     padx=10, pady=5, width=w,
                     activebackground=DARK, activeforeground=WHITE)

def sep(parent):
    return tk.Frame(parent, bg=BORDER, height=1)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PROGRAMACION POR METAS - SOFTWARE")
        self.configure(bg=BG)
        self.geometry("800x580")
        self.resizable(True, True)
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 800) // 2
        y = (self.winfo_screenheight() - 580) // 2
        self.geometry(f"800x580+{x}+{y}")

        self.n_var  = tk.IntVar(value=2)
        self.data   = None
        self.result = None

        self._frames = {}
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        for F in (PantallaInicio, PantallaProductos, PantallaMetas, PantallaPesos, PantallaResultados):
            f = F(container, self)
            self._frames[F] = f
            f.place(relwidth=1, relheight=1)

        self.mostrar(PantallaInicio)

    def mostrar(self, frame_class):
        f = self._frames[frame_class]
        if hasattr(f, "al_mostrar"):
            f.al_mostrar()
        f.lift()

    def resolver(self):
        pf = self._frames[PantallaProductos]
        mf = self._frames[PantallaMetas]
        wf = self._frames[PantallaPesos]
        try:
            n = self.n_var.get()
            self.data = ModelData(
                n=n,
                utilidades=[float(pf.v_util[i].get()) for i in range(n)],
                horas=     [float(pf.v_hora[i].get()) for i in range(n)],
                costos=    [float(pf.v_cost[i].get()) for i in range(n)],
                minimos=   [float(pf.v_mini[i].get()) for i in range(n)],
                meta_ganancia=   float(mf.v_g.get()),
                meta_horas=      float(mf.v_h.get()),
                meta_presupuesto=float(mf.v_p.get()),
                peso_over1= float(wf.o1.get()), peso_under1=float(wf.u1.get()),
                peso_over2= float(wf.o2.get()), peso_under2=float(wf.u2.get()),
                peso_over3= float(wf.o3.get()), peso_under3=float(wf.u3.get()),
            )
        except ValueError:
            messagebox.showerror("Error", "Todos los campos deben ser numericos.")
            return False
        self.result = solve(build(self.data), self.data)
        return True


class PantallaInicio(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        lbl(wrap, "Programación por metas", bold=True, size=20).pack(pady=(0, 4))
        lbl(wrap, "Modelo MBI", color=GRAY).pack(pady=(0, 30))

        sep(wrap).pack(fill="x", pady=(0, 24))

        lbl(wrap, "Numero de productos a analizar:", bold=True).pack(pady=(0, 8))

        row = tk.Frame(wrap, bg=BG)
        row.pack()
        tk.Spinbox(row, from_=MIN_PRODUCTOS, to=MAX_PRODUCTOS,
                   textvariable=app.n_var, width=4,
                   font=("Segoe UI", 16, "bold"),
                   justify="center", relief="solid", bd=1).pack()

        tk.Frame(wrap, bg=BG, height=20).pack()
        btn(wrap, "Comenzar →", lambda: app.mostrar(PantallaProductos), w=20).pack()


class PantallaProductos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.v_util = []
        self.v_hora = []
        self.v_cost = []
        self.v_mini = []

    def al_mostrar(self):
        for w in self.winfo_children():
            w.destroy()
        self._construir()

    def _construir(self):
        n = self.app.n_var.get()
        self.v_util = [tk.StringVar() for _ in range(n)]
        self.v_hora = [tk.StringVar() for _ in range(n)]
        self.v_cost = [tk.StringVar() for _ in range(n)]
        self.v_mini = [tk.StringVar() for _ in range(n)]

        for i in range(n):
            d = DEFAULTS_PRODUCTO[i] if i < len(DEFAULTS_PRODUCTO) else {"utilidad":0,"horas":0,"costo":0,"minimo":0}
            self.v_util[i].set(d["utilidad"])
            self.v_hora[i].set(d["horas"])
            self.v_cost[i].set(d["costo"])
            self.v_mini[i].set(d["minimo"])

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(20, 0))
        lbl(top, "Paso 1 - Datos por producto", bold=True, size=12).pack(side="left")
        sep(self).pack(fill="x", padx=24, pady=10)

        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0, 8))
        canvas.pack(fill="both", expand=True, padx=(24, 0))

        inner = tk.Frame(canvas, bg=BG)
        cw = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))

        header_row = tk.Frame(inner, bg=BG)
        header_row.pack(fill="x", pady=(0, 4))
        for txt, w in [("Producto", 8), ("Utilidad ($)", 14), ("Horas", 10), ("Costo ($)", 14), ("Min. prod.", 10)]:
            lbl(header_row, txt, color=GRAY, size=9, width=w).pack(side="left", padx=8)

        for i in range(n):
            row = tk.Frame(inner, bg=WHITE, bd=0,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=3, padx=2)
            lbl(row, f"X{i+1}", bold=True, color=BLUE).pack(side="left", padx=12)
            for var in (self.v_util[i], self.v_hora[i], self.v_cost[i], self.v_mini[i]):
                e = entry(row, var)
                e.configure(bg=WHITE)
                e.pack(side="left", padx=8, pady=8)

        sep(self).pack(fill="x", padx=24, pady=8)
        nav = tk.Frame(self, bg=BG)
        nav.pack(pady=(0, 16))
        btn(nav, "← Volver", lambda: self.app.mostrar(PantallaInicio), color=GRAY, w=10).pack(side="left", padx=6)
        btn(nav, "Siguiente →", lambda: self.app.mostrar(PantallaMetas), w=12).pack(side="left", padx=6)


class PantallaMetas(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        d = DEFAULTS_METAS
        self.v_g = tk.StringVar(value=d["ganancia"])
        self.v_h = tk.StringVar(value=d["horas"])
        self.v_p = tk.StringVar(value=d["presupuesto"])
        self._construir()

    def _construir(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.65)

        lbl(wrap, "Paso 2 - Metas objetivo", bold=True, size=12).pack(anchor="w", pady=(0, 4))
        sep(wrap).pack(fill="x", pady=8)
        lbl(wrap, "Define los valores que el modelo intentara alcanzar.", color=GRAY, size=9).pack(anchor="w", pady=(0, 16))

        for label, var in [
            ("Meta de Ganancia ($)",    self.v_g),
            ("Meta de Horas (hrs)",     self.v_h),
            ("Meta de Presupuesto ($)", self.v_p),
        ]:
            box = tk.Frame(wrap, bg=WHITE, bd=0,
                           highlightthickness=1, highlightbackground=BORDER)
            box.pack(fill="x", pady=5)
            lbl(box, label, bold=True).pack(anchor="w", padx=12, pady=(10, 2))
            entry(box, var, w=25).pack(anchor="w", padx=12, pady=(0, 10))

        sep(wrap).pack(fill="x", pady=12)
        nav = tk.Frame(wrap, bg=BG)
        nav.pack()
        btn(nav, "← Volver", lambda: self.app.mostrar(PantallaProductos), color=GRAY, w=10).pack(side="left", padx=6)
        btn(nav, "Siguiente →", lambda: self.app.mostrar(PantallaPesos), w=12).pack(side="left", padx=6)


class PantallaPesos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        d = DEFAULTS_PESOS
        self.o1, self.u1 = tk.StringVar(value=d["over1"]),  tk.StringVar(value=d["under1"])
        self.o2, self.u2 = tk.StringVar(value=d["over2"]),  tk.StringVar(value=d["under2"])
        self.o3, self.u3 = tk.StringVar(value=d["over3"]),  tk.StringVar(value=d["under3"])
        self._construir()

    def _construir(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75)

        lbl(wrap, "Paso 3 - Pesos de penalizacion", bold=True, size=12).pack(anchor="w", pady=(0, 4))
        sep(wrap).pack(fill="x", pady=8)
        lbl(wrap, "Peso 0 = esa desviacion no penaliza. Mayor peso = mas importante.", color=GRAY, size=9).pack(anchor="w", pady=(0, 12))

        grupos = [
            ("Ganancia",        self.o1, "OVER1 - superar meta",    self.u1, "UNDER1 - no alcanzar"),
            ("Horas de trabajo",self.o2, "OVER2 - exceder horas",   self.u2, "UNDER2 - quedar corto"),
            ("Presupuesto",     self.o3, "OVER3 - exceder presup.", self.u3, "UNDER3 - quedar corto"),
        ]

        for titulo, ov, ol, uv, ul in grupos:
            box = tk.Frame(wrap, bg=WHITE, bd=0,
                           highlightthickness=1, highlightbackground=BORDER)
            box.pack(fill="x", pady=5)
            lbl(box, titulo, bold=True).pack(anchor="w", padx=12, pady=(8, 6))

            row = tk.Frame(box, bg=WHITE)
            row.pack(fill="x", padx=12, pady=(0, 10))

            col1 = tk.Frame(row, bg=WHITE)
            col1.pack(side="left", expand=True, fill="x")
            lbl(col1, ol, color=YELLOW, size=9).pack(anchor="w")
            entry(col1, ov, w=12).pack(anchor="w", pady=4)

            col2 = tk.Frame(row, bg=WHITE)
            col2.pack(side="left", expand=True, fill="x")
            lbl(col2, ul, color=RED, size=9).pack(anchor="w")
            entry(col2, uv, w=12).pack(anchor="w", pady=4)

        sep(wrap).pack(fill="x", pady=12)
        nav = tk.Frame(wrap, bg=BG)
        nav.pack()
        btn(nav, "← Volver", lambda: self.app.mostrar(PantallaMetas), color=GRAY, w=10).pack(side="left", padx=6)
        btn(nav, "Resolver", self._resolver, color=GREEN, w=12).pack(side="left", padx=6)

    def _resolver(self):
        if self.app.resolver():
            self.app.mostrar(PantallaResultados)


class PantallaResultados(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def al_mostrar(self):
        for w in self.winfo_children():
            w.destroy()
        self._construir()

    def _construir(self):
        result = self.app.result
        data   = self.app.data

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(20, 0))
        lbl(top, "Resultados", bold=True, size=12).pack(side="left")
        sep(self).pack(fill="x", padx=24, pady=10)

        if not result.exitoso:
            lbl(self, f"Sin solucion: {result.mensaje}", color=RED, bold=True).pack(pady=40)
            btn(self, "← Volver", lambda: self.app.mostrar(PantallaPesos), color=GRAY).pack()
            return

        z_box = tk.Frame(self, bg=DARK, bd=0)
        z_box.pack(fill="x", padx=24, pady=(0, 10))
        lbl(z_box, "Funcion objetivo  Z =", color="#aaaaaa", size=9).pack(pady=(8, 0))
        lbl(z_box, f"{result.Z:,.2f}", color=WHITE, size=20, bold=True).pack(pady=(0, 8))

        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0, 6))
        canvas.pack(fill="both", expand=True, padx=24)

        body = tk.Frame(canvas, bg=BG)
        cw = canvas.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))

        lbl(body, "Producción recomendada", bold=True).pack(anchor="w", pady=(10, 6))
        x_row = tk.Frame(body, bg=BG)
        x_row.pack(anchor="w")
        for i, val in enumerate(result.X):
            card = tk.Frame(x_row, bg=WHITE, bd=0,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(side="left", padx=4, pady=2, ipadx=12, ipady=6)
            lbl(card, f"X{i+1} — Producto {i+1}", color=GRAY, size=9).pack()
            lbl(card, f"{val:,.2f}", color=BLUE, bold=True, size=13).pack()
            lbl(card, f"min: {data.minimos[i]:,.0f}", color=GRAY, size=8).pack()

        sep(body).pack(fill="x", pady=8)
        lbl(body, "Variables de desviacion", bold=True).pack(anchor="w", pady=(0, 6))
        d_row = tk.Frame(body, bg=BG)
        d_row.pack(anchor="w")
        dev_items = [
            ("OVER1",  result.over1,  "Ganancia supera",   YELLOW),
            ("UNDER1", result.under1, "Ganancia bajo",     RED),
            ("OVER2",  result.over2,  "Horas exceden",     YELLOW),
            ("UNDER2", result.under2, "Horas cortas",      RED),
            ("OVER3",  result.over3,  "Presup. excede",    YELLOW),
            ("UNDER3", result.under3, "Presup. corto",     RED),
        ]
        for nombre, val, desc, color in dev_items:
            c = color if val > 0.01 else BORDER
            card = tk.Frame(d_row, bg=WHITE, bd=0,
                            highlightthickness=1, highlightbackground=c)
            card.pack(side="left", padx=4, pady=2, ipadx=8, ipady=4)
            tc = color if val > 0.01 else GRAY
            lbl(card, nombre, color=tc, bold=True, size=9).pack()
            lbl(card, f"{val:,.2f}", color=tc, size=11, bold=True).pack()
            lbl(card, desc, color=GRAY, size=8).pack()

        sep(body).pack(fill="x", pady=8)
        lbl(body, "Analisis de metas", bold=True).pack(anchor="w", pady=(0, 6))

        th = tk.Frame(body, bg=DARK)
        th.pack(fill="x")
        for txt, w in [("Meta", 18), ("Alcanzado", 13), ("Objetivo", 13), ("Desviacion", 12), ("Estado", 15)]:
            lbl(th, txt, color="#aaaaaa", size=9, width=w).pack(side="left", padx=6, anchor="w", pady=4)

        estados = {"en_meta": (GREEN, "En meta"), "sobre": (YELLOW, "Sobre la meta"), "bajo": (RED, "Bajo la meta")}
        for i, row in enumerate(result.desviaciones):
            color, label = estados[row.estado]
            dev_str = f"{'+' if row.desviacion >= 0 else ''}{row.desviacion:,.0f}"
            bg = WHITE if i % 2 == 0 else "#f9fafb"
            tr = tk.Frame(body, bg=bg, bd=0,
                          highlightthickness=1, highlightbackground=BORDER)
            tr.pack(fill="x", pady=1)
            for txt, w, fc in [
                (row.nombre,             18, DARK),
                (f"{row.actual:,.0f}",   13, BLUE),
                (f"{row.objetivo:,.0f}", 13, DARK),
                (dev_str,                12, color),
                (label,                  15, color),
            ]:
                lbl(tr, txt, color=fc, size=9, width=w).pack(side="left", padx=6, anchor="w", pady=6)

        sep(body).pack(fill="x", pady=8)
        nav = tk.Frame(body, bg=BG)
        nav.pack(pady=(0, 16))
        btn(nav, "← Ajustar pesos", lambda: self.app.mostrar(PantallaPesos), color=GRAY, w=14).pack(side="left", padx=4)
        btn(nav, "Nuevo modelo", lambda: self.app.mostrar(PantallaInicio), color=GRAY, w=12).pack(side="left", padx=4)
        btn(nav, "Resolver de nuevo", self._re_resolver, color=BLUE, w=14).pack(side="left", padx=4)

    def _re_resolver(self):
        if self.app.resolver():
            self.al_mostrar()


def launch():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    launch()
