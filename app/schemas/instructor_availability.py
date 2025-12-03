from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import time


class InstructorAvailabilityBase(BaseModel):
    """Schema base para InstructorAvailability"""
    day_of_week: int = Field(..., ge=0, le=6, description="0=Domingo, 1=Segunda ... 6=Sábado")
    start_time: time
    end_time: time
    is_active: bool = True
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time deve ser maior que start_time')
        return v


class InstructorAvailabilityCreate(InstructorAvailabilityBase):
    """Schema para criação de InstructorAvailability"""
    instructor_id: int


class InstructorAvailabilityUpdate(BaseModel):
    """Schema para atualização de InstructorAvailability"""
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None


class InstructorAvailabilityResponse(InstructorAvailabilityBase):
    """Schema de resposta para InstructorAvailability"""
    id: int
    instructor_id: int
    
    class Config:
        from_attributes = True
