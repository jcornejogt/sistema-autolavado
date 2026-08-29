from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from database.database import Base


class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    telefono = Column(String(30), nullable=True)
    direccion = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)
