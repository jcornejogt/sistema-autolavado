import customtkinter as ctk
from tkinter import messagebox
import logging
import os
import sys

from license import licencia_valida

# Configurar logging
log_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if not licencia_valida():

    root = ctk.CTk()
    root.withdraw()

    messagebox.showerror(
        "Licencia vencida",
        "La licencia de este sistema ha expirado."
    )

    root.destroy()
    exit()

from database.database import Base, engine

from models.user import User
from models.employee import Employee
from models.attendance import Attendance
from models.servicio import Servicio
from models.accesorio import Accesorio
from models.sale import Sale
from models.sale_detail import SaleDetail

from controllers.user_controller import UserController

from views.login_view import LoginView
from views.main_view import MainView


Base.metadata.create_all(bind=engine)

UserController.crear_admin_por_defecto()

print("Base de datos creada correctamente.")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Sistema Autolavado")
        self.geometry("1200x700")
        self.resizable(True, True)
        self.state("zoomed")

        self.mostrar_login()

    def limpiar_ventana(self):

        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        LoginView(self, on_success=self.mostrar_main)

    def mostrar_main(self, usuario):

        self.limpiar_ventana()

        MainView(
            self,
            usuario_actual=usuario,
            cerrar_sesion_callback=self.mostrar_login
        ).pack(fill="both", expand=True)


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logging.error(f"Error en la aplicación: {e}", exc_info=True)
        root = ctk.CTk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"Ocurrió un error en la aplicación:\n\n{str(e)}\n\nRevisa el archivo app.log para más detalles."
        )
        root.destroy()