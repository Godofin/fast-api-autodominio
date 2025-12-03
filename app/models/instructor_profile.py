from sqlalchemy import Column, Integer, String, Text, DECIMAL, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TransmissionType(str, enum.Enum):
    """Enum para tipo de transmissão"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class ApprovalStatus(str, enum.Enum):
    """Enum para status de aprovação do instrutor"""
    PENDING = "pending"  # Aguardando aprovação
    APPROVED = "approved"  # Aprovado
    REJECTED = "rejected"  # Rejeitado
    UNDER_REVIEW = "under_review"  # Em análise


class InstructorProfile(Base):
    """Modelo de Perfil do Instrutor"""
    __tablename__ = "instructor_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(Text)
    credential_number = Column(String(100), unique=True, nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    car_model = Column(String(100))
    transmission = Column(Enum(TransmissionType), nullable=False)
    city = Column(String(100), nullable=False)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    approval_date = Column(DateTime)
    rejection_reason = Column(Text)  # Motivo da rejeição (se aplicável)
    
    # Relacionamentos
    user = relationship("User", back_populates="instructor_profile")
    availability = relationship("InstructorAvailability", back_populates="instructor", cascade="all, delete-orphan")
    time_off = relationship("InstructorTimeOff", back_populates="instructor", cascade="all, delete-orphan")
    documents = relationship("InstructorDocument", back_populates="instructor", cascade="all, delete-orphan")
