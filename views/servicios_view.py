import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.servicio_controller import ServicioController


class ServiciosView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.servicio_id = None

        ctk.CTkLabel(
            self, text="🚿 Servicios de Lavado", font=("Arial", 28, "bold")
        ).pack(pady=20)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20)

        ctk.CTkLabel(formulario, text="Nombre").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.nombre = ctk.CTkEntry(formulario, width=250)
        self.nombre.grid(row=0, column=1)

        ctk.CTkLabel(formulario, text="Precio").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.precio = ctk.CTkEntry(formulario, width=250)
        self.precio.grid(row=1, column=1)

        botones = ctk.CTkFrame(formulario, fg_color="transparent")
        botones.grid(row=2, column=0, columnspan=2, pady=20)

        self.btn_guardar = ctk.CTkButton(
            botones, text="Guardar", command=self.guardar
        )
        self.btn_guardar.pack(side="left", padx=5)

        ctk.CTkButton(
            botones,
            text="Eliminar",
            fg_color="red",
            hover_color="#990000",
            command=self.eliminar
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botones, text="Nuevo", command=self.limpiar
        ).pack(side="left", padx=5)

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "nombre", "precio"),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=300)
        self.tabla.column("precio", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar()

    def guardar(self):

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning("Validación", "Ingrese el nombre.")
            return

        try:
            precio = float(self.precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return

        if precio <= 0:
            messagebox.showwarning("Validación", "El precio debe ser mayor a cero.")
            return

        if self.servicio_id is None:
            ServicioController.guardar(nombre, precio)
            messagebox.showinfo("Servicio", "Servicio creado correctamente.")
        else:
            ServicioController.actualizar(self.servicio_id, nombre, precio)
            messagebox.showinfo("Servicio", "Servicio actualizado correctamente.")

        self.limpiar()
        self.cargar()

    def seleccionar(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)["values"]

        self.servicio_id = datos[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, datos[1])

        self.precio.delete(0, "end")
        self.precio.insert(0, datos[2])

        self.btn_guardar.configure(text="Actualizar")

    def eliminar(self):

        if self.servicio_id is None:
            messagebox.showwarning("Servicio", "Seleccione un servicio.")
            return

        if not messagebox.askyesno("Eliminar", "¿Desea eliminar este servicio?"):
            return

        ServicioController.eliminar(self.servicio_id)

        messagebox.showinfo("Servicio", "Servicio eliminado.")

        self.limpiar()
        self.cargar()

    def limpiar(self):

        self.servicio_id = None

        self.nombre.delete(0, "end")
        self.precio.delete(0, "end")

        self.btn_guardar.configure(text="Guardar")

        self.tabla.selection_remove(self.tabla.selection())

    def cargar(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for s in ServicioController.listar():

            self.tabla.insert(
                "", "end", values=(s.id, s.nombre, f"{s.precio:.2f}")
            )