from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class InstructorTimeOffBase(BaseModel):
    """Schema base para InstructorTimeOff"""
    date: date
    reason: Optional[str] = Field(None, max_length=255)


class InstructorTimeOffCreate(InstructorTimeOffBase):
    """Schema para criação de InstructorTimeOff"""
    instructor_id: int


class InstructorTimeOffUpdate(BaseModel):
    """Schema para atualização de InstructorTimeOff"""
    date: Optional[date] = None
    reason: Optional[str] = Field(None, max_length=255)


class InstructorTimeOffResponse(InstructorTimeOffBase):
    """Schema de resposta para InstructorTimeOff"""
    id: int
    instructor_id: int
    
    class Config:
        from_attributes = True
