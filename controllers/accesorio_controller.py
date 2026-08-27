from database.database import SessionLocal
from models.accesorio import Accesorio


class AccesorioController:

    @staticmethod
    def guardar(nombre, precio, stock):

        db = SessionLocal()

        try:

            accesorio = Accesorio(nombre=nombre, precio=precio, stock=stock)

            db.add(accesorio)
            db.commit()

        finally:

            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:

            return db.query(Accesorio).order_by(Accesorio.nombre).all()

        finally:

            db.close()

    @staticmethod
    def listar_disponibles():

        db = SessionLocal()

        try:

            return (
                db.query(Accesorio)
                .filter(Accesorio.stock > 0)
                .order_by(Accesorio.nombre)
                .all()
            )

        finally:

            db.close()

    @staticmethod
    def obtener_por_id(accesorio_id):

        db = SessionLocal()

        try:

            return db.query(Accesorio).filter(
                Accesorio.id == accesorio_id
            ).first()

        finally:

            db.close()

    @staticmethod
    def actualizar(accesorio_id, nombre, precio, stock):

        db = SessionLocal()

        try:

            accesorio = db.query(Accesorio).filter(
                Accesorio.id == accesorio_id
            ).first()

            if accesorio:

                accesorio.nombre = nombre
                accesorio.precio = precio
                accesorio.stock = stock

                db.commit()

        finally:

            db.close()

    @staticmethod
    def eliminar(accesorio_id):

        db = SessionLocal()

        try:

            accesorio = db.query(Accesorio).filter(
                Accesorio.id == accesorio_id
            ).first()

            if accesorio:

                db.delete(accesorio)
                db.commit()

        finally:

            db.close()