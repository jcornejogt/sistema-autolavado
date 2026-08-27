import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.employee_controller import EmployeeController
from controllers.servicio_controller import ServicioController
from controllers.accesorio_controller import AccesorioController
from controllers.sale_controller import SaleController


class SalesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.carrito = []

        ctk.CTkLabel(
            self, text="🛒 Registrar Venta", font=("Arial", 28, "bold")
        ).pack(pady=15)

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20)

        ctk.CTkLabel(top, text="Empleado que atiende:").pack(side="left", padx=10)

        self.empleado_combo = ctk.CTkComboBox(top, width=250, values=[])
        self.empleado_combo.pack(side="left", padx=10)

        self.cargar_empleados()

        contenedor = ctk.CTkFrame(self)
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        izquierda = ctk.CTkFrame(contenedor)
        izquierda.pack(side="left", fill="y", padx=10)

        ctk.CTkLabel(
            izquierda, text="Servicios de lavado", font=("Arial", 15, "bold")
        ).pack(pady=(10, 5))

        self.servicios_tree = ttk.Treeview(
            izquierda,
            columns=("id", "nombre", "precio"),
            show="headings",
            height=6
        )
        self.servicios_tree.heading("id", text="ID")
        self.servicios_tree.heading("nombre", text="Servicio")
        self.servicios_tree.heading("precio", text="Precio")
        self.servicios_tree.column("id", width=40)
        self.servicios_tree.column("nombre", width=140)
        self.servicios_tree.column("precio", width=70)
        self.servicios_tree.pack(padx=10)

        ctk.CTkButton(
            izquierda, text="Agregar lavado ➕", command=self.agregar_servicio
        ).pack(pady=10)

        ctk.CTkLabel(
            izquierda, text="Accesorios", font=("Arial", 15, "bold")
        ).pack(pady=(15, 5))

        self.accesorios_tree = ttk.Treeview(
            izquierda,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            height=6
        )
        self.accesorios_tree.heading("id", text="ID")
        self.accesorios_tree.heading("nombre", text="Accesorio")
        self.accesorios_tree.heading("precio", text="Precio")
        self.accesorios_tree.heading("stock", text="Stock")
        self.accesorios_tree.column("id", width=40)
        self.accesorios_tree.column("nombre", width=120)
        self.accesorios_tree.column("precio", width=60)
        self.accesorios_tree.column("stock", width=50)
        self.accesorios_tree.pack(padx=10)

        cant_frame = ctk.CTkFrame(izquierda, fg_color="transparent")
        cant_frame.pack(pady=5)

        ctk.CTkLabel(cant_frame, text="Cantidad:").pack(side="left", padx=5)

        self.cantidad_entry = ctk.CTkEntry(cant_frame, width=60)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.pack(side="left")

        ctk.CTkButton(
            izquierda, text="Agregar accesorio ➕", command=self.agregar_accesorio
        ).pack(pady=10)

        derecha = ctk.CTkFrame(contenedor)
        derecha.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            derecha, text="Detalle de venta", font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.detalle = ttk.Treeview(
            derecha,
            columns=("nombre", "cantidad", "precio", "subtotal"),
            show="headings"
        )
        self.detalle.heading("nombre", text="Nombre")
        self.detalle.heading("cantidad", text="Cantidad")
        self.detalle.heading("precio", text="Precio")
        self.detalle.heading("subtotal", text="Subtotal")
        self.detalle.pack(fill="both", expand=True, padx=10)

        self.total_label = ctk.CTkLabel(
            derecha, text="Total: C$ 0.00", font=("Arial", 22, "bold")
        )
        self.total_label.pack(pady=15)

        ctk.CTkButton(
            derecha,
            text="Finalizar Venta",
            fg_color="green",
            command=self.finalizar
        ).pack(pady=10)

        self.cargar_servicios()
        self.cargar_accesorios()

    def cargar_empleados(self):

        empleados = EmployeeController.listar_activos()

        self.empleados_map = {e.nombre: e.id for e in empleados}

        self.empleado_combo.configure(values=list(self.empleados_map.keys()))

        if empleados:
            self.empleado_combo.set(empleados[0].nombre)

    def cargar_servicios(self):

        for fila in self.servicios_tree.get_children():
            self.servicios_tree.delete(fila)

        for s in ServicioController.listar():

            self.servicios_tree.insert(
                "", "end", values=(s.id, s.nombre, f"{s.precio:.2f}")
            )

    def cargar_accesorios(self):

        for fila in self.accesorios_tree.get_children():
            self.accesorios_tree.delete(fila)

        for a in AccesorioController.listar_disponibles():

            self.accesorios_tree.insert(
                "", "end", values=(a.id, a.nombre, f"{a.precio:.2f}", a.stock)
            )

    def agregar_servicio(self):

        seleccionado = self.servicios_tree.focus()

        if not seleccionado:
            messagebox.showwarning("Venta", "Seleccione un servicio de lavado.")
            return

        datos = self.servicios_tree.item(seleccionado)["values"]

        item = {
            "tipo": "servicio",
            "referencia_id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2]),
            "cantidad": 1
        }

        self.carrito.append(item)

        self.actualizar_carrito()

    def agregar_accesorio(self):

        seleccionado = self.accesorios_tree.focus()

        if not seleccionado:
            messagebox.showwarning("Venta", "Seleccione un accesorio.")
            return

        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Venta", "La cantidad debe ser mayor a cero.")
            return

        datos = self.accesorios_tree.item(seleccionado)["values"]

        item = {
            "tipo": "accesorio",
            "referencia_id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2]),
            "cantidad": cantidad
        }

        self.carrito.append(item)

        self.actualizar_carrito()

    def actualizar_carrito(self):

        for fila in self.detalle.get_children():
            self.detalle.delete(fila)

        total = 0

        for item in self.carrito:

            subtotal = item["precio"] * item["cantidad"]
            total += subtotal

            self.detalle.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    item["cantidad"],
                    f"{item['precio']:.2f}",
                    f"{subtotal:.2f}"
                )
            )

        self.total_label.configure(text=f"Total: C$ {total:.2f}")

    def finalizar(self):

        if len(self.carrito) == 0:
            messagebox.showwarning("Venta", "No hay nada en el carrito.")
            return

        nombre_empleado = self.empleado_combo.get()

        if nombre_empleado not in self.empleados_map:
            messagebox.showwarning("Venta", "Seleccione un empleado válido.")
            return

        employee_id = self.empleados_map[nombre_empleado]

        items = [
            {
                "tipo": item["tipo"],
                "referencia_id": item["referencia_id"],
                "cantidad": item["cantidad"]
            }
            for item in self.carrito
        ]

        try:
            SaleController.registrar_venta(employee_id, items)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Venta", "Venta registrada correctamente.")

        self.carrito.clear()

        self.actualizar_carrito()
        self.cargar_accesorios()