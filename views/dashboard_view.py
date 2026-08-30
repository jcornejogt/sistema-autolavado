import customtkinter as ctk

from controllers.employee_controller import EmployeeController
from controllers.report_controller import ReportController


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.crear_dashboard()

    def crear_dashboard(self):

        self.configure(fg_color="#f3f8ff")

        ctk.CTkLabel(
            self,
            text="🏠 Dashboard",
            font=("Arial", 30, "bold"),
            text_color="#102a43"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="Bienvenido al Sistema Autolavado",
            font=("Arial", 18),
            text_color="#26456a"
        ).pack(pady=(0, 20))

        reporte = ReportController.reporte_dia()

        tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        tarjetas.pack(fill="x", padx=20)

        self.crear_tarjeta(
            tarjetas, "👷 Empleados activos",
            str(len(EmployeeController.listar_activos()))
        ).pack(side="left", padx=10)

        self.crear_tarjeta(
            tarjetas, "🛒 Ventas Hoy",
            str(reporte["cantidad_ventas"]),
            ancho=280,
            alto=135
        ).pack(side="left", padx=10)

        self.crear_tarjeta(
            tarjetas, "💵 Total Hoy",
            f"C$ {reporte['total_dia']:.2f}",
            ancho=260,
            alto=135
        ).pack(side="left", padx=10)

    def crear_tarjeta(self, master, titulo, valor, ancho=220, alto=120):

        card = ctk.CTkFrame(master, width=ancho, height=alto, corner_radius=15)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text=titulo, font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card, text=valor, font=("Arial", 30, "bold")
        ).pack()

        return card