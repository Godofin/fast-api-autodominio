from sqlalchemy import Column, Integer, String, Text, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class TransmissionType(str, enum.Enum):
    """Enum para tipo de transmissão"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"


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
    
    # Relacionamentos
    user = relationship("User", back_populates="instructor_profile")
    availability = relationship("InstructorAvailability", back_populates="instructor", cascade="all, delete-orphan")
    time_off = relationship("InstructorTimeOff", back_populates="instructor", cascade="all, delete-orphan")
