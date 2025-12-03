from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class InstructorAvailability(Base):
    """Modelo de Disponibilidade do Instrutor"""
    __tablename__ = "instructor_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, ForeignKey("instructor_profiles.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Domingo, 1=Segunda ... 6=Sábado
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relacionamento
    instructor = relationship("InstructorProfile", back_populates="availability")
