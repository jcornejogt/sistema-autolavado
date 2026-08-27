from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class SaleDetail(Base):

    __tablename__ = "sale_details"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)

    tipo = Column(String(20), nullable=False)  # "servicio" o "accesorio"
    referencia_id = Column(Integer, nullable=False)
    nombre = Column(String(100), nullable=False)

    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    subtotal = Column(Float, nullable=False)
    comision = Column(Float, nullable=False, default=0)

    venta = relationship("Sale", back_populates="detalles")