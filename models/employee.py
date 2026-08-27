from sqlalchemy import Column, Integer, String, Boolean

from database.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)