from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class InstructorTimeOff(Base):
    """Modelo de Exceções na Agenda do Instrutor"""
    __tablename__ = "instructor_time_off"
    
    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, ForeignKey("instructor_profiles.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    reason = Column(String(255))
    
    # Relacionamento
    instructor = relationship("InstructorProfile", back_populates="time_off")
