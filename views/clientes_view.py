import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.cliente_controller import ClienteController


class ClientesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.cliente_id_seleccionado = None

        ctk.CTkLabel(
            self,
            text="👥 Clientes",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20)

        ctk.CTkLabel(formulario, text="Nombre").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.nombre_entry = ctk.CTkEntry(formulario, width=280)
        self.nombre_entry.grid(row=0, column=1)

        ctk.CTkLabel(formulario, text="Documento").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.documento_entry = ctk.CTkEntry(formulario, width=280)
        self.documento_entry.grid(row=1, column=1)

        ctk.CTkLabel(formulario, text="Teléfono").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.telefono_entry = ctk.CTkEntry(formulario, width=280)
        self.telefono_entry.grid(row=2, column=1)

        ctk.CTkLabel(formulario, text="Dirección").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.direccion_entry = ctk.CTkEntry(formulario, width=280)
        self.direccion_entry.grid(row=3, column=1)

        botones = ctk.CTkFrame(formulario, fg_color="transparent")
        botones.grid(row=4, column=0, columnspan=2, pady=20)

        self.btn_guardar = ctk.CTkButton(botones, text="Guardar", command=self.guardar_cliente)
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            fg_color="red",
            hover_color="#990000",
            command=self.eliminar_cliente
        )
        self.btn_eliminar.pack(side="left", padx=5)

        ctk.CTkButton(botones, text="Nuevo", command=self.limpiar).pack(side="left", padx=5)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "nombre", "documento", "telefono", "direccion"),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("documento", text="Documento")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("direccion", text="Dirección")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=220)
        self.tabla.column("documento", width=120)
        self.tabla.column("telefono", width=120)
        self.tabla.column("direccion", width=220)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        self.cargar_clientes()

    def guardar_cliente(self):

        nombre = self.nombre_entry.get().strip()
        documento = self.documento_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        direccion = self.direccion_entry.get().strip()

        if not nombre or not documento:
            messagebox.showwarning("Validación", "Ingrese nombre y documento.")
            return

        try:
            if self.cliente_id_seleccionado is None:
                ClienteController.crear(nombre, documento, telefono, direccion)
                messagebox.showinfo("Cliente", "Cliente creado correctamente.")
            else:
                ClienteController.actualizar(
                    self.cliente_id_seleccionado,
                    nombre,
                    documento,
                    telefono,
                    direccion
                )
                messagebox.showinfo("Cliente", "Cliente actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.limpiar()
        self.cargar_clientes()

    def seleccionar_cliente(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)["values"]
        self.cliente_id_seleccionado = datos[0]

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, datos[1])

        self.documento_entry.delete(0, "end")
        self.documento_entry.insert(0, datos[2])

        self.telefono_entry.delete(0, "end")
        self.telefono_entry.insert(0, datos[3])

        self.direccion_entry.delete(0, "end")
        self.direccion_entry.insert(0, datos[4])

        self.btn_guardar.configure(text="Actualizar")

    def eliminar_cliente(self):

        if self.cliente_id_seleccionado is None:
            messagebox.showwarning("Cliente", "Seleccione un cliente.")
            return

        if not messagebox.askyesno("Eliminar", "¿Desea eliminar este cliente?"):
            return

        try:
            ClienteController.eliminar(self.cliente_id_seleccionado)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Cliente", "Cliente eliminado.")

        self.limpiar()
        self.cargar_clientes()

    def limpiar(self):

        self.cliente_id_seleccionado = None
        self.nombre_entry.delete(0, "end")
        self.documento_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.direccion_entry.delete(0, "end")
        self.btn_guardar.configure(text="Guardar")
        self.tabla.selection_remove(self.tabla.selection())

    def cargar_clientes(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for cliente in ClienteController.listar():
            self.tabla.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.documento,
                    cliente.telefono,
                    cliente.direccion,
                )
            )
