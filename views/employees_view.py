import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.employee_controller import EmployeeController
from controllers.attendance_controller import AttendanceController


class EmployeesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self, text="👷 Empleados y Asistencia", font=("Arial", 28, "bold")
        ).pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20)

        ctk.CTkLabel(formulario, text="Nombre del empleado").pack(
            side="left", padx=10
        )

        self.nombre_entry = ctk.CTkEntry(formulario, width=250)
        self.nombre_entry.pack(side="left", padx=10)

        ctk.CTkButton(
            formulario, text="➕ Agregar empleado", command=self.agregar
        ).pack(side="left", padx=10)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "nombre", "entrada", "salida"),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("entrada", text="Entrada hoy")
        self.tabla.heading("salida", text="Salida hoy")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=250)
        self.tabla.column("entrada", width=150, anchor="center")
        self.tabla.column("salida", width=150, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(pady=10)

        ctk.CTkButton(
            botones,
            text="🟢 Marcar entrada",
            fg_color="green",
            command=self.marcar_entrada
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botones,
            text="🔴 Marcar salida",
            fg_color="red",
            hover_color="#990000",
            command=self.marcar_salida
        ).pack(side="left", padx=10)

        self.cargar()

    def agregar(self):

        nombre = self.nombre_entry.get().strip()

        if nombre == "":
            messagebox.showwarning("Empleado", "Ingrese el nombre.")
            return

        EmployeeController.crear(nombre)

        self.nombre_entry.delete(0, "end")

        self.cargar()

    def obtener_seleccionado(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Asistencia", "Seleccione un empleado.")
            return None

        return self.tabla.item(seleccionado)["values"][0]

    def marcar_entrada(self):

        employee_id = self.obtener_seleccionado()

        if employee_id is None:
            return

        try:
            AttendanceController.marcar_entrada(employee_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Asistencia", "Entrada marcada.")
        self.cargar()

    def marcar_salida(self):

        employee_id = self.obtener_seleccionado()

        if employee_id is None:
            return

        try:
            AttendanceController.marcar_salida(employee_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Asistencia", "Salida marcada.")
        self.cargar()

    def cargar(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for item in AttendanceController.listar_hoy():

            entrada = (
                item["hora_entrada"].strftime("%H:%M")
                if item["hora_entrada"] else "--"
            )

            salida = (
                item["hora_salida"].strftime("%H:%M")
                if item["hora_salida"] else "--"
            )

            self.tabla.insert(
                "",
                "end",
                values=(item["employee_id"], item["nombre"], entrada, salida)
            )