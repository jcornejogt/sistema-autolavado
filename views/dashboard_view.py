import customtkinter as ctk

from controllers.employee_controller import EmployeeController
from controllers.report_controller import ReportController


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.crear_dashboard()

    def crear_dashboard(self):

        ctk.CTkLabel(
            self, text="🏠 Dashboard", font=("Arial", 30, "bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="Bienvenido al Sistema Autolavado",
            font=("Arial", 18)
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
            str(reporte["cantidad_ventas"])
        ).pack(side="left", padx=10)

        self.crear_tarjeta(
            tarjetas, "💵 Total Hoy",
            f"C$ {reporte['total_dia']:.2f}"
        ).pack(side="left", padx=10)

    def crear_tarjeta(self, master, titulo, valor):

        card = ctk.CTkFrame(master, width=220, height=120, corner_radius=15)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text=titulo, font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card, text=valor, font=("Arial", 30, "bold")
        ).pack()

        return card