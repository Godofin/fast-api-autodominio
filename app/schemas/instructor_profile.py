from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.models.instructor_profile import TransmissionType, ApprovalStatus


class InstructorProfileBase(BaseModel):
    """Schema base para InstructorProfile"""
    bio: Optional[str] = None
    credential_number: str = Field(..., min_length=1, max_length=100)
    hourly_rate: Decimal = Field(..., gt=0)
    car_model: Optional[str] = Field(None, max_length=100)
    transmission: TransmissionType
    city: str = Field(..., min_length=1, max_length=100)


class InstructorProfileCreate(InstructorProfileBase):
    """Schema para criação de InstructorProfile"""
    user_id: int


class InstructorProfileUpdate(BaseModel):
    """Schema para atualização de InstructorProfile"""
    bio: Optional[str] = None
    hourly_rate: Optional[Decimal] = Field(None, gt=0)
    car_model: Optional[str] = Field(None, max_length=100)
    transmission: Optional[TransmissionType] = None
    city: Optional[str] = Field(None, min_length=1, max_length=100)


class InstructorProfileResponse(InstructorProfileBase):
    """Schema de resposta para InstructorProfile"""
    id: int
    user_id: int
    approval_status: ApprovalStatus
    approval_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    
    class Config:
        from_attributes = True
