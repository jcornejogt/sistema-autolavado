import customtkinter as ctk
from tkinter import ttk

from controllers.report_controller import ReportController


class ReportsView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self, text="📊 Reporte del Día", font=("Arial", 28, "bold")
        ).pack(pady=20)

        reporte = ReportController.reporte_dia()

        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.pack(fill="x", padx=20)

        self.tarjeta(
            resumen, "🛒 Ventas hoy", str(reporte["cantidad_ventas"])
        ).pack(side="left", padx=10)

        self.tarjeta(
            resumen, "💵 Total del día", f"C$ {reporte['total_dia']:.2f}"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            self,
            text="Ganancia por empleado (comisión)",
            font=("Arial", 18, "bold")
        ).pack(pady=(25, 10))

        tabla = ttk.Treeview(
            self,
            columns=("nombre", "ventas", "vendido", "comision"),
            show="headings",
            height=10
        )

        tabla.heading("nombre", text="Empleado")
        tabla.heading("ventas", text="# Ventas")
        tabla.heading("vendido", text="Total vendido")
        tabla.heading("comision", text="Comisión ganada")

        tabla.column("nombre", width=200)
        tabla.column("ventas", width=100, anchor="center")
        tabla.column("vendido", width=150, anchor="center")
        tabla.column("comision", width=150, anchor="center")

        tabla.pack(fill="both", expand=True, padx=20, pady=(10, 5))

        for emp in reporte["por_empleado"]:

            tabla.insert(
                "",
                "end",
                values=(
                    emp["nombre"],
                    emp["cantidad_ventas"],
                    f"C$ {emp['total_vendido']:.2f}",
                    f"C$ {emp['comision']:.2f}"
                )
            )

        ctk.CTkLabel(
            self,
            text="Servicios vendidos por empleado",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 5))

        servicios_tabla = ttk.Treeview(
            self,
            columns=("empleado", "servicio", "cantidad", "subtotal"),
            show="headings",
            height=10
        )

        servicios_tabla.heading("empleado", text="Empleado")
        servicios_tabla.heading("servicio", text="Servicio")
        servicios_tabla.heading("cantidad", text="Cantidad")
        servicios_tabla.heading("subtotal", text="Subtotal")

        servicios_tabla.column("empleado", width=180)
        servicios_tabla.column("servicio", width=220)
        servicios_tabla.column("cantidad", width=100, anchor="center")
        servicios_tabla.column("subtotal", width=140, anchor="center")

        servicios_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        hay_servicios = False

        for emp in reporte["por_empleado"]:
            for servicio in emp["servicios"]:
                hay_servicios = True
                servicios_tabla.insert(
                    "",
                    "end",
                    values=(
                        emp["nombre"],
                        servicio["nombre"],
                        servicio["cantidad"],
                        f"C$ {servicio['subtotal']:.2f}"
                    )
                )

        if not hay_servicios:
            ctk.CTkLabel(
                self,
                text="Aún no hay servicios vendidos hoy.",
                font=("Arial", 14)
            ).pack(pady=10)

        if not reporte["por_empleado"]:

            ctk.CTkLabel(
                self,
                text="Aún no hay ventas registradas hoy.",
                font=("Arial", 14)
            ).pack(pady=20)

    def tarjeta(self, master, titulo, valor):

        card = ctk.CTkFrame(master, width=220, height=110, corner_radius=15)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text=titulo, font=("Arial", 15, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card, text=valor, font=("Arial", 26, "bold")
        ).pack()

        return card