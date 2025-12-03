from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class AppointmentStatus(str, enum.Enum):
    """Enum para status do agendamento"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Appointment(Base):
    """Modelo de Agendamento/Aula"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)
    location_pickup = Column(String(255))
    notes = Column(Text)
    
    # Relacionamentos
    student = relationship("User", foreign_keys=[student_id], back_populates="student_appointments")
    instructor = relationship("User", foreign_keys=[instructor_id], back_populates="instructor_appointments")
