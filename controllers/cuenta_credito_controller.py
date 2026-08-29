import os
from datetime import datetime

from database.database import SessionLocal
from models.cliente import Cliente
from models.cuenta_credito import CuentaCredito, CuentaCreditoDetalle


class CuentaCreditoController:

    @staticmethod
    def registrar_cuenta(cliente_id, descripcion, items, observacion=""):

        db = SessionLocal()

        try:

            cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

            if cliente is None:
                raise ValueError("Debe seleccionar un cliente válido.")

            if not items:
                raise ValueError("Debe agregar al menos un concepto para la cuenta.")

            total = 0.0
            detalles = []

            for item in items:

                concepto = str(item["concepto"]).strip()
                cantidad = int(item["cantidad"])
                precio = float(item["precio_unitario"])

                if concepto == "":
                    raise ValueError("Cada concepto necesita un nombre.")

                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor que cero.")

                subtotal = cantidad * precio
                total += subtotal

                detalles.append({
                    "concepto": concepto,
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "subtotal": subtotal,
                })

            cuenta = CuentaCredito(
                cliente_id=cliente_id,
                descripcion=descripcion.strip() or "Cuenta de crédito",
                total=total,
                saldo=total,
                estado="Pendiente",
                observacion=observacion.strip() or None,
                fecha_apertura=datetime.now()
            )

            db.add(cuenta)
            db.flush()

            for detalle in detalles:
                db.add(CuentaCreditoDetalle(
                    cuenta_id=cuenta.id,
                    concepto=detalle["concepto"],
                    cantidad=detalle["cantidad"],
                    precio_unitario=detalle["precio_unitario"],
                    subtotal=detalle["subtotal"],
                ))

            db.commit()
            return cuenta

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:
            return db.query(CuentaCredito).order_by(CuentaCredito.fecha_apertura.desc()).all()
        finally:
            db.close()

    @staticmethod
    def listar_por_cliente(cliente_id):

        db = SessionLocal()

        try:
            return db.query(CuentaCredito).filter(
                CuentaCredito.cliente_id == cliente_id
            ).order_by(CuentaCredito.fecha_apertura.desc()).all()
        finally:
            db.close()

    @staticmethod
    def obtener_cuenta(cuenta_id):

        db = SessionLocal()

        try:
            cuenta = db.query(CuentaCredito).filter(CuentaCredito.id == cuenta_id).first()
            if cuenta is None:
                return None

            detalles = db.query(CuentaCreditoDetalle).filter(
                CuentaCreditoDetalle.cuenta_id == cuenta_id
            ).order_by(CuentaCreditoDetalle.id).all()

            return {
                "cuenta": cuenta,
                "detalles": detalles,
                "cliente": cuenta.cliente
            }
        finally:
            db.close()

    @staticmethod
    def generar_recibo(cuenta_id):

        db = SessionLocal()

        try:
            cuenta = db.query(CuentaCredito).filter(CuentaCredito.id == cuenta_id).first()

            if cuenta is None:
                raise ValueError("La cuenta no existe.")

            detalles = db.query(CuentaCreditoDetalle).filter(
                CuentaCreditoDetalle.cuenta_id == cuenta_id
            ).order_by(CuentaCreditoDetalle.id).all()

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            recibos_dir = os.path.join(base_dir, "recibos")
            os.makedirs(recibos_dir, exist_ok=True)

            nombre_archivo = f"recibo_{cuenta.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta = os.path.join(recibos_dir, nombre_archivo)

            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("========================================\n")
                archivo.write("          RECIBO DE LIQUIDACIÓN         \n")
                archivo.write("========================================\n")
                archivo.write(f"Cliente: {cuenta.cliente.nombre}\n")
                archivo.write(f"Documento: {cuenta.cliente.documento}\n")
                archivo.write(f"Descripción: {cuenta.descripcion}\n")
                archivo.write(f"Fecha: {cuenta.fecha_liquidacion.strftime('%d/%m/%Y %H:%M:%S') if cuenta.fecha_liquidacion else datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                archivo.write("\nDetalle:\n")

                for item in detalles:
                    archivo.write(
                        f"- {item.concepto} x{item.cantidad} @ {item.precio_unitario:.2f} = {item.subtotal:.2f}\n"
                    )

                archivo.write(f"\nTOTAL: C$ {cuenta.total:.2f}\n")
                archivo.write("\nEstado: Liquidada\n")
                archivo.write("========================================\n")

            return ruta

        finally:
            db.close()

    @staticmethod
    def liquidar_cuenta(cuenta_id):

        db = SessionLocal()

        try:
            cuenta = db.query(CuentaCredito).filter(CuentaCredito.id == cuenta_id).first()

            if cuenta is None:
                raise ValueError("La cuenta no existe.")

            if cuenta.estado == "Liquidada":
                raise ValueError("La cuenta ya está liquidada.")

            cuenta.saldo = 0.0
            cuenta.estado = "Liquidada"
            cuenta.fecha_liquidacion = datetime.now()

            db.commit()
            return cuenta

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
