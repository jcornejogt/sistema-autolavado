from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_entrada = Column(DateTime, nullable=True)
    hora_salida = Column(DateTime, nullable=True)

    empleado = relationship("Employee")