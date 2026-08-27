from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base


class Sale(Base):

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float, nullable=False)

    empleado = relationship("Employee")

    detalles = relationship(
        "SaleDetail",
        back_populates="venta",
        cascade="all, delete"
    )