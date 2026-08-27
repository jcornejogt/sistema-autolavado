from datetime import date, datetime, timedelta

from database.database import SessionLocal
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.employee import Employee


class ReportController:

    @staticmethod
    def reporte_dia(fecha=None):

        if fecha is None:
            fecha = date.today()

        inicio = datetime.combine(fecha, datetime.min.time())
        fin = inicio + timedelta(days=1)

        db = SessionLocal()

        try:

            ventas = db.query(Sale).filter(
                Sale.fecha >= inicio,
                Sale.fecha < fin
            ).all()

            total_dia = sum(v.total for v in ventas)
            cantidad_ventas = len(ventas)

            empleados = db.query(Employee).all()

            por_empleado = []

            for emp in empleados:

                ventas_emp = [v for v in ventas if v.employee_id == emp.id]

                if not ventas_emp:
                    continue

                total_vendido = sum(v.total for v in ventas_emp)

                comision_total = 0

                for v in ventas_emp:

                    detalles = db.query(SaleDetail).filter(
                        SaleDetail.sale_id == v.id
                    ).all()

                    comision_total += sum(d.comision for d in detalles)

                por_empleado.append({
                    "nombre": emp.nombre,
                    "cantidad_ventas": len(ventas_emp),
                    "total_vendido": total_vendido,
                    "comision": comision_total
                })

            por_empleado.sort(
                key=lambda x: x["total_vendido"],
                reverse=True
            )

            return {
                "fecha": fecha,
                "total_dia": total_dia,
                "cantidad_ventas": cantidad_ventas,
                "por_empleado": por_empleado
            }

        finally:

            db.close()