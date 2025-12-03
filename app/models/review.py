from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Review(Base):
    """Modelo de Avaliação/Review"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 a 5 estrelas
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraint para garantir rating entre 1 e 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
    
    # Relacionamentos
    appointment = relationship("Appointment", backref="review")
    student = relationship("User", foreign_keys=[student_id])
    instructor = relationship("User", foreign_keys=[instructor_id])
