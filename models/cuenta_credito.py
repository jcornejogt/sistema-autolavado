from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class CuentaCredito(Base):

    __tablename__ = "cuentas_credito"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    descripcion = Column(String(200), nullable=False, default="Cuenta de crédito")
    total = Column(Float, nullable=False, default=0.0)
    saldo = Column(Float, nullable=False, default=0.0)
    estado = Column(String(20), nullable=False, default="Pendiente")
    observacion = Column(String(200), nullable=True)
    fecha_apertura = Column(DateTime, default=datetime.now)
    fecha_liquidacion = Column(DateTime, nullable=True)

    cliente = relationship("Cliente")
    detalles = relationship(
        "CuentaCreditoDetalle",
        back_populates="cuenta",
        cascade="all, delete-orphan"
    )


class CuentaCreditoDetalle(Base):

    __tablename__ = "cuentas_credito_detalles"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas_credito.id"), nullable=False)
    concepto = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False, default=0.0)
    subtotal = Column(Float, nullable=False, default=0.0)

    cuenta = relationship("CuentaCredito", back_populates="detalles")
