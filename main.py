import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LinearFunctionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Funciones Lineales f(x) = mx + b")
        self.geometry("850x650")
        self.minsize(700, 500)
        self.canvas_widget = None  # Referencia al lienzo de Matplotlib
        self._setup_ui()

    def _setup_ui(self):
        # ── Panel de entrada de datos ──
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.m_label = ctk.CTkLabel(self.input_frame, text="Pendiente (m):")
        self.m_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.m_entry = ctk.CTkEntry(self.input_frame, width=150)
        self.m_entry.grid(row=0, column=1, padx=10, pady=15)

        self.b_label = ctk.CTkLabel(self.input_frame, text="Término indep. (b):")
        self.b_label.grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.b_entry = ctk.CTkEntry(self.input_frame, width=150)
        self.b_entry.grid(row=1, column=1, padx=10, pady=15)

        # Botones de acción (lado a lado)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.plot_btn = ctk.CTkButton(
            self.input_frame, text="Generar y Graficar", command=self._generate_plot
        )
        self.plot_btn.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.clear_btn = ctk.CTkButton(
            self.input_frame, text="🗑️ Limpiar Todo", 
            fg_color="red", hover_color="darkred", command=self._clear_all
        )
        self.clear_btn.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack(pady=5)

        # ── Panel del gráfico ──
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def _validate_inputs(self):
        """Valida que los valores sean numéricos y finitos."""
        m_str = self.m_entry.get().strip()
        b_str = self.b_entry.get().strip()

        if not m_str or not b_str:
            raise ValueError("⚠️ Los campos 'm' y 'b' no pueden estar vacíos.")

        try:
            m = float(m_str)
            b = float(b_str)
        except ValueError:
            raise ValueError("⚠️ 'm' y 'b' deben ser números válidos.")

        if not (math.isfinite(m) and math.isfinite(b)):
            raise ValueError("⚠️ 'm' y 'b' deben ser valores finitos (no inf o nan).")

        return m, b

    def _generate_plot(self):
        try:
            m, b = self._validate_inputs()
        except ValueError as e:
            self.status_label.configure(text=str(e), text_color="red")
            return

        self.status_label.configure(text="✅ Procesando datos y graficando...", text_color="green")
        self.update_idletasks()

        # Limpiar gráfico anterior si existe
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            self.canvas_widget = None

        # ── 1. Generación de datos con NumPy ──
        x = np.linspace(-10, 10, 500)
        y = m * x + b

        # ── 2. Uso de Pandas para estructurar los datos ──
        df = pd.DataFrame({"x": x, "y": y})
        df["ecuacion"] = f"{m}·x + {b}"

        # ── 3. Creación de la figura con Matplotlib ──
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.plot(x, y, label=f"f(x) = {m}x + {b}", color="#1f77b4", linewidth=2.5)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("f(x)", fontsize=12)
        ax.set_title("Función Lineal", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        ax.grid(True, linestyle=":", alpha=0.6)
        fig.tight_layout()

        # ── 4. Integración en CustomTkinter ──
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)

        self.status_label.configure(
            text=f"✅ Función graficada: f(x) = {m}x + {b}  |  Puntos procesados: {len(df)}",
            text_color="green"
        )

    def _clear_all(self):
        """Limpia campos de entrada, estado y la gráfica actual."""
        # 1. Vaciar campos de texto
        self.m_entry.delete(0, "end")
        self.b_entry.delete(0, "end")
        
        # 2. Limpiar mensaje de estado
        self.status_label.configure(text="")
        
        # 3. Destruir canvas si existe
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            self.canvas_widget = None
            
        self.status_label.configure(
            text="🧹 Datos y gráfica limpiados. Ingresa nuevos valores.",
            text_color="blue"
        )

if __name__ == "__main__":
    app = LinearFunctionApp()
    app.mainloop()
