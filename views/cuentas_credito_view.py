import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.cliente_controller import ClienteController
from controllers.cuenta_credito_controller import CuentaCreditoController


class CuentasCreditoView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.items = []
        self.cuenta_id_seleccionado = None
        self.clientes_map = {}

        ctk.CTkLabel(
            self,
            text="💳 Cuentas / Crédito",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        self.cargar_clientes()

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20)

        ctk.CTkLabel(top, text="Cliente:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.cliente_combo = ctk.CTkComboBox(top, width=280, values=[])
        self.cliente_combo.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(top, text="Descripción:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.descripcion_entry = ctk.CTkEntry(top, width=280)
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(top, text="Observación:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.observacion_entry = ctk.CTkEntry(top, width=280)
        self.observacion_entry.grid(row=2, column=1, padx=10, pady=8)

        detalle_frame = ctk.CTkFrame(self)
        detalle_frame.pack(fill="both", expand=True, padx=20, pady=10)

        izquierda = ctk.CTkFrame(detalle_frame)
        izquierda.pack(side="left", fill="y", padx=10)

        ctk.CTkLabel(izquierda, text="Agregar concepto", font=("Arial", 16, "bold")).pack(pady=(10, 8))

        ctk.CTkLabel(izquierda, text="Concepto").pack(anchor="w", padx=10)
        self.concepto_entry = ctk.CTkEntry(izquierda, width=260)
        self.concepto_entry.pack(padx=10, pady=(0, 8))

        ctk.CTkLabel(izquierda, text="Cantidad").pack(anchor="w", padx=10)
        self.cantidad_entry = ctk.CTkEntry(izquierda, width=260)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.pack(padx=10, pady=(0, 8))

        ctk.CTkLabel(izquierda, text="Precio unitario").pack(anchor="w", padx=10)
        self.precio_entry = ctk.CTkEntry(izquierda, width=260)
        self.precio_entry.pack(padx=10, pady=(0, 10))

        ctk.CTkButton(izquierda, text="Agregar al detalle ➕", command=self.agregar_item).pack(pady=5)

        derecha = ctk.CTkFrame(detalle_frame)
        derecha.pack(side="left", fill="both", expand=True, padx=10)

        ctk.CTkLabel(derecha, text="Detalle de la cuenta", font=("Arial", 16, "bold")).pack(pady=(10, 8))

        self.detalle_tree = ttk.Treeview(
            derecha,
            columns=("concepto", "cantidad", "precio", "subtotal"),
            show="headings",
            height=10
        )
        self.detalle_tree.heading("concepto", text="Concepto")
        self.detalle_tree.heading("cantidad", text="Cantidad")
        self.detalle_tree.heading("precio", text="Precio")
        self.detalle_tree.heading("subtotal", text="Subtotal")
        self.detalle_tree.column("concepto", width=200)
        self.detalle_tree.column("cantidad", width=90, anchor="center")
        self.detalle_tree.column("precio", width=90, anchor="center")
        self.detalle_tree.column("subtotal", width=100, anchor="center")
        self.detalle_tree.pack(fill="both", expand=True, padx=10)

        self.total_label = ctk.CTkLabel(
            derecha,
            text="Total: C$ 0.00",
            font=("Arial", 22, "bold")
        )
        self.total_label.pack(pady=10)

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(botones, text="Guardar cuenta", command=self.guardar_cuenta)
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_liquidar = ctk.CTkButton(
            botones,
            text="Liquidar cuenta",
            fg_color="green",
            hover_color="#006600",
            command=self.liquidar_cuenta
        )
        self.btn_liquidar.pack(side="left", padx=5)

        ctk.CTkButton(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        cuentas_frame = ctk.CTkFrame(self)
        cuentas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        ctk.CTkLabel(cuentas_frame, text="Cuentas registradas", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self.cuentas_tree = ttk.Treeview(
            cuentas_frame,
            columns=("id", "cliente", "descripcion", "total", "estado"),
            show="headings",
            height=8
        )
        self.cuentas_tree.heading("id", text="ID")
        self.cuentas_tree.heading("cliente", text="Cliente")
        self.cuentas_tree.heading("descripcion", text="Descripción")
        self.cuentas_tree.heading("total", text="Total")
        self.cuentas_tree.heading("estado", text="Estado")
        self.cuentas_tree.column("id", width=50, anchor="center")
        self.cuentas_tree.column("cliente", width=180)
        self.cuentas_tree.column("descripcion", width=220)
        self.cuentas_tree.column("total", width=100, anchor="center")
        self.cuentas_tree.column("estado", width=100, anchor="center")
        self.cuentas_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.cuentas_tree.bind("<<TreeviewSelect>>", self.seleccionar_cuenta)

        self.actualizar_detalle()
        self.cargar_cuentas()

    def cargar_clientes(self):

        clientes = ClienteController.listar()
        self.clientes_map = {f"{c.nombre} ({c.documento})": c.id for c in clientes}

        self.cliente_combo.configure(values=list(self.clientes_map.keys()))

        if self.clientes_map:
            self.cliente_combo.set(next(iter(self.clientes_map.keys())))

    def agregar_item(self):

        concepto = self.concepto_entry.get().strip()
        cantidad_texto = self.cantidad_entry.get().strip()
        precio_texto = self.precio_entry.get().strip()

        if not concepto:
            messagebox.showwarning("Cuenta", "Ingrese un concepto.")
            return

        try:
            cantidad = int(cantidad_texto)
            precio = float(precio_texto)
        except ValueError:
            messagebox.showerror("Error", "La cantidad y el precio deben ser válidos.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Cuenta", "La cantidad debe ser mayor que cero.")
            return

        if precio < 0:
            messagebox.showwarning("Cuenta", "El precio no puede ser negativo.")
            return

        self.items.append({
            "concepto": concepto,
            "cantidad": cantidad,
            "precio_unitario": precio,
        })

        self.concepto_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")
        self.precio_entry.delete(0, "end")

        self.actualizar_detalle()

    def actualizar_detalle(self):

        for fila in self.detalle_tree.get_children():
            self.detalle_tree.delete(fila)

        total = 0

        for item in self.items:
            subtotal = item["cantidad"] * item["precio_unitario"]
            total += subtotal
            self.detalle_tree.insert(
                "",
                "end",
                values=(
                    item["concepto"],
                    item["cantidad"],
                    f"{item['precio_unitario']:.2f}",
                    f"{subtotal:.2f}"
                )
            )

        self.total_label.configure(text=f"Total: C$ {total:.2f}")

    def guardar_cuenta(self):

        if not self.clientes_map:
            messagebox.showwarning("Cuenta", "Primero debe registrar al menos un cliente.")
            return

        if not self.items:
            messagebox.showwarning("Cuenta", "Agregue al menos un concepto a la cuenta.")
            return

        cliente_nombre = self.cliente_combo.get()
        cliente_id = self.clientes_map.get(cliente_nombre)

        if cliente_id is None:
            messagebox.showwarning("Cuenta", "Seleccione un cliente válido.")
            return

        descripcion = self.descripcion_entry.get().strip() or "Cuenta de crédito"
        observacion = self.observacion_entry.get().strip()

        try:
            cuenta = CuentaCreditoController.registrar_cuenta(
                cliente_id,
                descripcion,
                self.items,
                observacion
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.cuenta_id_seleccionado = cuenta.id
        self.limpiar()
        self.cargar_cuentas()
        messagebox.showinfo("Cuenta", "Cuenta creada correctamente.")

    def seleccionar_cuenta(self, event):

        seleccionado = self.cuentas_tree.focus()

        if not seleccionado:
            return

        datos = self.cuentas_tree.item(seleccionado)["values"]
        self.cuenta_id_seleccionado = datos[0]

    def liquidar_cuenta(self):

        if self.cuenta_id_seleccionado is None:
            messagebox.showwarning("Cuenta", "Seleccione una cuenta de la lista para liquidarla.")
            return

        if not messagebox.askyesno("Liquidación", "¿Desea liquidar esta cuenta y generar el recibo?"):
            return

        try:
            cuenta = CuentaCreditoController.liquidar_cuenta(self.cuenta_id_seleccionado)
            recibo_ruta = CuentaCreditoController.generar_recibo(cuenta.id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.cargar_cuentas()
        messagebox.showinfo(
            "Liquidación",
            f"Cuenta liquidada correctamente.\nRecibo generado:\n{recibo_ruta}"
        )
        self.cuenta_id_seleccionado = None

    def limpiar(self):

        self.items = []
        self.cuenta_id_seleccionado = None
        self.descripcion_entry.delete(0, "end")
        self.observacion_entry.delete(0, "end")
        self.concepto_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")
        self.precio_entry.delete(0, "end")
        self.actualizar_detalle()

        if self.clientes_map:
            self.cliente_combo.set(next(iter(self.clientes_map.keys())))

    def cargar_cuentas(self):

        for fila in self.cuentas_tree.get_children():
            self.cuentas_tree.delete(fila)

        for cuenta in CuentaCreditoController.listar():
            cliente_nombre = cuenta.cliente.nombre if cuenta.cliente else "Sin cliente"
            self.cuentas_tree.insert(
                "",
                "end",
                values=(
                    cuenta.id,
                    cliente_nombre,
                    cuenta.descripcion,
                    f"C$ {cuenta.total:.2f}",
                    cuenta.estado,
                )
            )
