from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    """Schema base para Review"""
    rating: int = Field(..., ge=1, le=5, description="Avaliação de 1 a 5 estrelas")
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Schema para criação de Review"""
    appointment_id: int
    instructor_id: int


class ReviewUpdate(BaseModel):
    """Schema para atualização de Review"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    """Schema de resposta para Review"""
    id: int
    appointment_id: int
    student_id: int
    instructor_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class InstructorRatingStats(BaseModel):
    """Schema para estatísticas de avaliação do instrutor"""
    instructor_id: int
    average_rating: float
    total_reviews: int
    rating_distribution: dict  # {1: count, 2: count, ...}
