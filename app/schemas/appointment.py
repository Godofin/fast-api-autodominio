from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    """Schema base para Appointment"""
    start_date: datetime
    end_date: datetime
    location_pickup: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError('end_date deve ser maior que start_date')
        return v


class AppointmentCreate(AppointmentBase):
    """Schema para criação de Appointment"""
    student_id: int
    instructor_id: int


class AppointmentUpdate(BaseModel):
    """Schema para atualização de Appointment"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    location_pickup: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    """Schema de resposta para Appointment"""
    id: int
    student_id: int
    instructor_id: int
    status: AppointmentStatus
    
    class Config:
        from_attributes = True
