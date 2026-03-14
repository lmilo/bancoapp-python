import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from banco import Banco

BG        = "#0D1B2A"
SIDEBAR   = "#1B2A3B"
CARD      = "#1E2F42"
ACCENT    = "#00C896"
DANGER    = "#E05C5C"
TEXT      = "#E8EDF2"
SUBTEXT   = "#8FA3B1"
BORDER    = "#2E4259"
HEADER_BG = "#132030"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUB   = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_MONO  = ("Consolas", 9)

banco = Banco("BancoApp")


def make_entry(parent, placeholder=""):
    frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    entry = tk.Entry(frame, bg=CARD, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", font=FONT_SUB)
    entry.pack(fill="x", padx=8, pady=6)
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=SUBTEXT)
        def on_focus_in(e, en=entry, ph=placeholder):
            if en.get() == ph:
                en.delete(0, "end")
                en.config(fg=TEXT)
        def on_focus_out(e, en=entry, ph=placeholder):
            if not en.get():
                en.insert(0, ph)
                en.config(fg=SUBTEXT)
        entry.bind("<FocusIn>",  on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    return frame, entry

def lbl(parent, text, font=FONT_LABEL, fg=TEXT):
    tk.Label(parent, text=text, bg=parent["bg"], fg=fg, font=font, anchor="w").pack(fill="x", pady=2)

def btn(parent, text, command, color=ACCENT, fg=BG):
    b = tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                  activebackground=color, font=FONT_BOLD, relief="flat",
                  cursor="hand2", padx=14, pady=8)
    b.pack(fill="x", pady=4)
    return b

def card(parent):
    return tk.Frame(parent, bg=CARD, padx=24, pady=20)

def show_msg(title, msg, error=False):
    (messagebox.showerror if error else messagebox.showinfo)(title, msg)


class Vista(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)

    def _title(self, text, icon=""):
        tk.Label(self, text=f"{icon}  {text}", bg=BG, fg=TEXT,
                 font=FONT_TITLE, anchor="w").pack(fill="x", padx=30, pady=(24, 4))
        tk.Frame(self, bg=ACCENT, height=3).pack(fill="x", padx=30, pady=(0, 18))


class VistaDashboard(Vista):
    def __init__(self, parent):
        super().__init__(parent)
        self._title("Dashboard", "")
        cuentas = banco.listar_cuentas()
        total   = sum(c.consultar_saldo() for c in cuentas)
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=30, pady=8)
        for titulo, valor, color in [
            ("Cuentas",     str(len(cuentas)),   ACCENT),
            ("Saldo Total", f"${total:,.2f}",     "#5B9BFF"),
        ]:
            c = tk.Frame(row, bg=CARD, padx=20, pady=16)
            c.pack(side="left", expand=True, fill="both", padx=8)
            tk.Label(c, text=titulo, bg=CARD, fg=SUBTEXT, font=FONT_LABEL).pack(anchor="w")
            tk.Label(c, text=valor,  bg=CARD, fg=color,
                     font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(4,0))


class VistaCrearCuenta(Vista):
    def __init__(self, parent, on_created=None):
        super().__init__(parent)
        self.on_created = on_created
        self._title("Crear Cuenta", "+")
        c = card(self)
        c.pack(padx=30, fill="x")
        lbl(c, "Numero de cuenta", FONT_BOLD, SUBTEXT)
        _, self.e_num = make_entry(c, "Ej: 001")
        self.e_num.master.pack(fill="x", pady=(0,10))
        lbl(c, "Titular", FONT_BOLD, SUBTEXT)
        _, self.e_tit = make_entry(c, "Nombre completo")
        self.e_tit.master.pack(fill="x", pady=(0,10))
        lbl(c, "Saldo inicial ($)", FONT_BOLD, SUBTEXT)
        _, self.e_sal = make_entry(c, "0.00")
        self.e_sal.master.pack(fill="x", pady=(0,16))
        btn(c, "Crear Cuenta", self._crear)

    def _crear(self):
        num = self.e_num.get().strip()
        tit = self.e_tit.get().strip()
        sal_txt = self.e_sal.get().strip()
        if num in ("", "Ej: 001") or tit in ("", "Nombre completo"):
            show_msg("Error", "Completa todos los campos.", error=True); return
        try:
            sal = float(sal_txt) if sal_txt not in ("", "0.00") else 0.0
            banco.crear_cuenta(num, tit, sal)
            show_msg("Exito", f"Cuenta {num} creada para {tit}.")
            if self.on_created: self.on_created()
        except (ValueError, TypeError) as ex:
            show_msg("Error", str(ex), error=True)


class VistaOperacion(Vista):
    def __init__(self, parent, modo="depositar"):
        super().__init__(parent)
        self.modo = modo
        icono  = "+" if modo == "depositar" else "-"
        titulo = "Depositar" if modo == "depositar" else "Retirar"
        self._title(titulo, icono)
        c = card(self)
        c.pack(padx=30, fill="x")
        lbl(c, "Numero de cuenta", FONT_BOLD, SUBTEXT)
        _, self.e_num   = make_entry(c, "Ej: 001")
        self.e_num.master.pack(fill="x", pady=(0,10))
        lbl(c, "Monto ($)", FONT_BOLD, SUBTEXT)
        _, self.e_monto = make_entry(c, "0.00")
        self.e_monto.master.pack(fill="x", pady=(0,16))
        color = ACCENT if modo == "depositar" else DANGER
        btn(c, titulo, self._operar, color=color)

    def _operar(self):
        num = self.e_num.get().strip()
        try:
            monto  = float(self.e_monto.get().strip())
            cuenta = banco.buscar_cuenta(num)
            if self.modo == "depositar":
                cuenta.depositar(monto)
                show_msg("Exito", f"Deposito de ${monto:,.2f} realizado.")
            else:
                cuenta.retirar(monto)
                show_msg("Exito", f"Retiro de ${monto:,.2f} realizado.")
        except (KeyError, ValueError, TypeError) as ex:
            show_msg("Error", str(ex), error=True)


class VistaConsultar(Vista):
    def __init__(self, parent):
        super().__init__(parent)
        self._title("Consultar Saldo", "?")
        c = card(self)
        c.pack(padx=30, fill="x")
        lbl(c, "Numero de cuenta", FONT_BOLD, SUBTEXT)
        _, self.e_num = make_entry(c, "Ej: 001")
        self.e_num.master.pack(fill="x", pady=(0,16))
        btn(c, "Consultar", self._consultar, color="#5B9BFF", fg=TEXT)
        self.res = tk.Frame(c, bg=CARD)
        self.res.pack(fill="x", pady=(8,0))

    def _consultar(self):
        for w in self.res.winfo_children(): w.destroy()
        num = self.e_num.get().strip()
        try:
            cuenta = banco.buscar_cuenta(num)
            info = tk.Frame(self.res, bg=HEADER_BG, padx=16, pady=14)
            info.pack(fill="x")
            tk.Label(info, text=cuenta.mostrar_info(), bg=HEADER_BG, fg=TEXT,
                     font=FONT_SUB, justify="left").pack(anchor="w")
            hist = cuenta.obtener_historial()
            if hist:
                tk.Label(self.res, text="Historial", bg=CARD, fg=SUBTEXT,
                         font=FONT_BOLD).pack(anchor="w", pady=(12,4))
                box = tk.Text(self.res, bg=HEADER_BG, fg=TEXT, font=FONT_MONO,
                              height=min(len(hist), 8), relief="flat")
                box.pack(fill="x")
                for linea in hist:
                    box.insert("end", linea + "\n")
                box.config(state="disabled")
        except KeyError as ex:
            show_msg("Error", str(ex), error=True)


class VistaListar(Vista):
    def __init__(self, parent):
        super().__init__(parent)
        self._title("Todas las Cuentas", "=")
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=30)
        header = tk.Frame(frame, bg=HEADER_BG)
        header.pack(fill="x")
        for col, w in [("Numero", 12), ("Titular", 25), ("Saldo", 15)]:
            tk.Label(header, text=col, bg=HEADER_BG, fg=ACCENT,
                     font=FONT_BOLD, width=w, anchor="center").pack(side="left", padx=2, pady=8)
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas, bg=BG)
        self.rows_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for i, c in enumerate(banco.listar_cuentas()):
            bg_row = CARD if i % 2 == 0 else "#182636"
            row = tk.Frame(self.rows_frame, bg=bg_row)
            row.pack(fill="x")
            for val, w in [(c.numero_cuenta, 12), (c.titular, 25),
                           (f"${c.consultar_saldo():,.2f}", 15)]:
                tk.Label(row, text=val, bg=bg_row, fg=TEXT,
                         font=FONT_SUB, width=w, anchor="center").pack(side="left", padx=2, pady=6)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BancoApp")
        self.geometry("980x640")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self._build()
        self._show("dashboard")

    def _build(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="BancoApp", bg=SIDEBAR, fg=ACCENT,
                 font=("Segoe UI", 15, "bold")).pack(pady=(28, 20))
        self._nav_btns = {}
        for texto, key in [
            ("Dashboard",       "dashboard"),
            ("Crear Cuenta",    "crear"),
            ("Depositar",       "depositar"),
            ("Retirar",         "retirar"),
            ("Consultar Saldo", "consultar"),
            ("Listar Cuentas",  "listar"),
        ]:
            b = tk.Button(self.sidebar, text=texto, bg=SIDEBAR, fg=TEXT,
                          font=FONT_SUB, relief="flat", anchor="w", padx=20,
                          cursor="hand2", activebackground=CARD,
                          command=lambda k=key: self._show(k))
            b.pack(fill="x", pady=2)
            self._nav_btns[key] = b
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _show(self, key):
        for w in self.content.winfo_children():
            w.destroy()
        for k, b in self._nav_btns.items():
            b.config(bg=ACCENT if k == key else SIDEBAR,
                     fg=BG    if k == key else TEXT)
        vistas = {
            "dashboard": lambda: VistaDashboard(self.content),
            "crear":     lambda: VistaCrearCuenta(self.content,
                             on_created=lambda: self._show("dashboard")),
            "depositar": lambda: VistaOperacion(self.content, "depositar"),
            "retirar":   lambda: VistaOperacion(self.content, "retirar"),
            "consultar": lambda: VistaConsultar(self.content),
            "listar":    lambda: VistaListar(self.content),
        }
        vistas[key]().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
