from sqlalchemy import Column, Integer, String, Float

from database.database import Base


class Servicio(Base):

    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)