from database.database import SessionLocal
from models.cliente import Cliente


class ClienteController:

    @staticmethod
    def crear(nombre, documento, telefono="", direccion=""):

        db = SessionLocal()

        try:

            nombre = nombre.strip()
            documento = documento.strip()

            if not nombre or not documento:
                raise ValueError("Nombre y documento son obligatorios.")

            existe = db.query(Cliente).filter(
                Cliente.documento == documento
            ).first()

            if existe:
                raise ValueError("Ya existe un cliente con ese documento.")

            cliente = Cliente(
                nombre=nombre,
                documento=documento,
                telefono=telefono.strip(),
                direccion=direccion.strip()
            )

            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return cliente

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:
            return db.query(Cliente).filter(Cliente.activo.is_(True)).order_by(Cliente.nombre).all()
        finally:
            db.close()

    @staticmethod
    def obtener_por_id(cliente_id):

        db = SessionLocal()

        try:
            return db.query(Cliente).filter(Cliente.id == cliente_id).first()
        finally:
            db.close()

    @staticmethod
    def actualizar(cliente_id, nombre, documento, telefono="", direccion=""):

        db = SessionLocal()

        try:

            cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

            if cliente is None:
                raise ValueError("El cliente no existe.")

            duplicado = db.query(Cliente).filter(
                Cliente.documento == documento,
                Cliente.id != cliente_id
            ).first()

            if duplicado:
                raise ValueError("Ya existe otro cliente con ese documento.")

            cliente.nombre = nombre.strip()
            cliente.documento = documento.strip()
            cliente.telefono = telefono.strip()
            cliente.direccion = direccion.strip()

            db.commit()
            return cliente

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def eliminar(cliente_id):

        db = SessionLocal()

        try:

            cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

            if cliente is None:
                raise ValueError("El cliente no existe.")

            cliente.activo = False
            db.commit()
            return True

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
