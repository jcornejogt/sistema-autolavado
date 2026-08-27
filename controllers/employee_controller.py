from database.database import SessionLocal
from models.employee import Employee


class EmployeeController:

    @staticmethod
    def crear(nombre):

        db = SessionLocal()

        try:

            empleado = Employee(nombre=nombre, activo=True)

            db.add(empleado)
            db.commit()

        finally:

            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:

            return db.query(Employee).order_by(Employee.nombre).all()

        finally:

            db.close()

    @staticmethod
    def listar_activos():

        db = SessionLocal()

        try:

            return (
                db.query(Employee)
                .filter(Employee.activo == True)
                .order_by(Employee.nombre)
                .all()
            )

        finally:

            db.close()

    @staticmethod
    def actualizar(employee_id, nombre, activo):

        db = SessionLocal()

        try:

            empleado = db.query(Employee).filter(
                Employee.id == employee_id
            ).first()

            if empleado:

                empleado.nombre = nombre
                empleado.activo = activo

                db.commit()

        finally:

            db.close()

    @staticmethod
    def eliminar(employee_id):

        db = SessionLocal()

        try:

            empleado = db.query(Employee).filter(
                Employee.id == employee_id
            ).first()

            if empleado:

                db.delete(empleado)
                db.commit()

        finally:

            db.close()