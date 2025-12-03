from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Schema base para User"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole
    profile_photo: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """Schema para criação de User"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema para atualização de User"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=6)
    profile_photo: Optional[str] = Field(None, max_length=500)


class UserResponse(UserBase):
    """Schema de resposta para User"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
