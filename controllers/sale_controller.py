from database.database import SessionLocal
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.servicio import Servicio
from models.accesorio import Accesorio


COMISION_SERVICIO = 0.40
COMISION_ACCESORIO = 0.00


class SaleController:

    @staticmethod
    def registrar_venta(employee_id, items):
        """
        items: lista de diccionarios:
        {"tipo": "servicio"|"accesorio", "referencia_id": int, "cantidad": int}
        """

        db = SessionLocal()

        try:

            if not items:
                raise Exception("Agregue al menos un servicio o accesorio.")

            total = 0
            detalles_data = []

            for item in items:

                if item["tipo"] == "servicio":

                    servicio = db.query(Servicio).filter(
                        Servicio.id == item["referencia_id"]
                    ).first()

                    if servicio is None:
                        raise Exception("Servicio no encontrado.")

                    subtotal = servicio.precio * item["cantidad"]
                    comision = subtotal * COMISION_SERVICIO

                    detalles_data.append({
                        "tipo": "servicio",
                        "referencia_id": servicio.id,
                        "nombre": servicio.nombre,
                        "precio": servicio.precio,
                        "cantidad": item["cantidad"],
                        "subtotal": subtotal,
                        "comision": comision
                    })

                    total += subtotal

                elif item["tipo"] == "accesorio":

                    accesorio = db.query(Accesorio).filter(
                        Accesorio.id == item["referencia_id"]
                    ).first()

                    if accesorio is None:
                        raise Exception("Accesorio no encontrado.")

                    if accesorio.stock < item["cantidad"]:
                        raise Exception(
                            f"No hay suficiente stock de '{accesorio.nombre}'."
                        )

                    subtotal = accesorio.precio * item["cantidad"]
                    comision = subtotal * COMISION_ACCESORIO

                    detalles_data.append({
                        "tipo": "accesorio",
                        "referencia_id": accesorio.id,
                        "nombre": accesorio.nombre,
                        "precio": accesorio.precio,
                        "cantidad": item["cantidad"],
                        "subtotal": subtotal,
                        "comision": comision
                    })

                    total += subtotal

                    accesorio.stock -= item["cantidad"]

            venta = Sale(employee_id=employee_id, total=total)

            db.add(venta)
            db.flush()

            for d in detalles_data:

                detalle = SaleDetail(
                    sale_id=venta.id,
                    tipo=d["tipo"],
                    referencia_id=d["referencia_id"],
                    nombre=d["nombre"],
                    precio=d["precio"],
                    cantidad=d["cantidad"],
                    subtotal=d["subtotal"],
                    comision=d["comision"]
                )

                db.add(detalle)

            db.commit()

            return venta.id

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def obtener_venta(venta_id):

        db = SessionLocal()

        try:

            venta = db.query(Sale).filter(Sale.id == venta_id).first()

            if venta is None:
                return None

            detalles = db.query(SaleDetail).filter(
                SaleDetail.sale_id == venta_id
            ).all()

            items = []

            for d in detalles:

                items.append({
                    "nombre": d.nombre,
                    "cantidad": d.cantidad,
                    "precio": d.precio,
                    "subtotal": d.subtotal
                })

            return {
                "id": venta.id,
                "fecha": venta.fecha,
                "total": venta.total,
                "empleado_nombre": venta.empleado.nombre,
                "items": items
            }

        finally:

            db.close()