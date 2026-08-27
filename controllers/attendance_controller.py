from datetime import date, datetime

from database.database import SessionLocal
from models.attendance import Attendance
from models.employee import Employee


class AttendanceController:

    @staticmethod
    def obtener_registro_hoy(employee_id):

        db = SessionLocal()

        try:

            return db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.fecha == date.today()
            ).first()

        finally:

            db.close()

    @staticmethod
    def marcar_entrada(employee_id):

        db = SessionLocal()

        try:

            registro = db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.fecha == date.today()
            ).first()

            if registro and registro.hora_entrada:
                raise Exception("Este empleado ya marcó entrada hoy.")

            if registro is None:

                registro = Attendance(
                    employee_id=employee_id,
                    fecha=date.today(),
                    hora_entrada=datetime.now()
                )

                db.add(registro)

            else:

                registro.hora_entrada = datetime.now()

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def marcar_salida(employee_id):

        db = SessionLocal()

        try:

            registro = db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.fecha == date.today()
            ).first()

            if registro is None or registro.hora_entrada is None:
                raise Exception("Este empleado no ha marcado entrada hoy.")

            if registro.hora_salida:
                raise Exception("Este empleado ya marcó salida hoy.")

            registro.hora_salida = datetime.now()

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def listar_hoy():

        db = SessionLocal()

        try:

            empleados = db.query(Employee).filter(
                Employee.activo == True
            ).order_by(Employee.nombre).all()

            resultado = []

            for emp in empleados:

                registro = db.query(Attendance).filter(
                    Attendance.employee_id == emp.id,
                    Attendance.fecha == date.today()
                ).first()

                resultado.append({
                    "employee_id": emp.id,
                    "nombre": emp.nombre,
                    "hora_entrada": registro.hora_entrada if registro else None,
                    "hora_salida": registro.hora_salida if registro else None
                })

            return resultado

        finally:

            db.close()