from database.database import SessionLocal
from models.servicio import Servicio


class ServicioController:

    @staticmethod
    def guardar(nombre, precio):

        db = SessionLocal()

        try:

            servicio = Servicio(nombre=nombre, precio=precio)

            db.add(servicio)
            db.commit()

        finally:

            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:

            return db.query(Servicio).order_by(Servicio.precio).all()

        finally:

            db.close()

    @staticmethod
    def obtener_por_id(servicio_id):

        db = SessionLocal()

        try:

            return db.query(Servicio).filter(
                Servicio.id == servicio_id
            ).first()

        finally:

            db.close()

    @staticmethod
    def actualizar(servicio_id, nombre, precio):

        db = SessionLocal()

        try:

            servicio = db.query(Servicio).filter(
                Servicio.id == servicio_id
            ).first()

            if servicio:

                servicio.nombre = nombre
                servicio.precio = precio

                db.commit()

        finally:

            db.close()

    @staticmethod
    def eliminar(servicio_id):

        db = SessionLocal()

        try:

            servicio = db.query(Servicio).filter(
                Servicio.id == servicio_id
            ).first()

            if servicio:

                db.delete(servicio)
                db.commit()

        finally:

            db.close()