import customtkinter as ctk
from datetime import datetime

from views.dashboard_view import DashboardView
from views.servicios_view import ServiciosView
from views.accesorios_view import AccesoriosView
from views.employees_view import EmployeesView
from views.sales_view import SalesView
from views.reports_view import ReportsView
from views.users_view import UsersView


class MainView(ctk.CTkFrame):

    def __init__(self, master, usuario_actual, cerrar_sesion_callback=None):
        super().__init__(master)

        self.usuario_actual = usuario_actual
        self.cerrar_sesion_callback = cerrar_sesion_callback

        self.pack(fill="both", expand=True)

        self.crear_menu()
        self.crear_contenedor()
        self.crear_barra_estado()

        self.dashboard()

        self.actualizar_hora()

    def crear_menu(self):

        self.menu = ctk.CTkFrame(self, width=220)
        self.menu.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.menu, text="🚗 Autolavado", font=("Arial", 22, "bold")
        ).pack(pady=30)

        rol_actual = self.usuario_actual["rol"]

        botones = [
            ("🏠 Dashboard", self.dashboard, None),
            ("🛒 Ventas", self.ventas, None),
            ("🚿 Servicios", self.servicios, ["Admin"]),
            ("🧴 Accesorios", self.accesorios, ["Admin"]),
            ("👷 Empleados", self.empleados, ["Admin"]),
            ("📊 Reportes", self.reportes, ["Admin"]),
            ("👤 Usuarios", self.usuarios, ["Admin"])
        ]

        for texto, comando, roles_permitidos in botones:

            if roles_permitidos is not None and rol_actual not in roles_permitidos:
                continue

            ctk.CTkButton(
                self.menu, text=texto, width=180, height=40, command=comando
            ).pack(pady=8, padx=20)

    def crear_contenedor(self):

        self.contenido = ctk.CTkFrame(self)
        self.contenido.pack(
            side="left", fill="both", expand=True, padx=10, pady=10
        )

    def crear_barra_estado(self):

        self.estado = ctk.CTkFrame(self, height=35)
        self.estado.pack(side="bottom", fill="x")

        ctk.CTkLabel(
            self.estado,
            text=f"👤 {self.usuario_actual['nombre']} ({self.usuario_actual['rol']})"
        ).pack(side="left", padx=20)

        self.hora_label = ctk.CTkLabel(self.estado, text="")
        self.hora_label.pack(side="right", padx=20)

        ctk.CTkButton(
            self.estado,
            text="Cerrar sesión",
            width=110,
            height=24,
            fg_color="gray",
            command=self.cerrar_sesion
        ).pack(side="right", padx=10)

    def cerrar_sesion(self):

        if self.cerrar_sesion_callback:
            self.cerrar_sesion_callback()

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def dashboard(self):

        self.limpiar_contenido()
        DashboardView(self.contenido).pack(fill="both", expand=True)

    def ventas(self):

        self.limpiar_contenido()
        SalesView(self.contenido).pack(fill="both", expand=True)

    def servicios(self):

        self.limpiar_contenido()
        ServiciosView(self.contenido).pack(fill="both", expand=True)

    def accesorios(self):

        self.limpiar_contenido()
        AccesoriosView(self.contenido).pack(fill="both", expand=True)

    def empleados(self):

        self.limpiar_contenido()
        EmployeesView(self.contenido).pack(fill="both", expand=True)

    def reportes(self):

        self.limpiar_contenido()
        ReportsView(self.contenido).pack(fill="both", expand=True)

    def usuarios(self):

        self.limpiar_contenido()

        UsersView(
            self.contenido, usuario_actual=self.usuario_actual
        ).pack(fill="both", expand=True)

    def actualizar_hora(self):

        ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

        self.hora_label.configure(text=ahora)

        self.after(1000, self.actualizar_hora)