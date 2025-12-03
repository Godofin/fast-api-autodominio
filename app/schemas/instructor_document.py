from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.instructor_document import DocumentType


class InstructorDocumentBase(BaseModel):
    """Schema base para InstructorDocument"""
    document_type: DocumentType


class InstructorDocumentCreate(InstructorDocumentBase):
    """Schema para criação de InstructorDocument"""
    instructor_id: int
    file_path: str
    original_filename: Optional[str] = None


class InstructorDocumentResponse(InstructorDocumentBase):
    """Schema de resposta para InstructorDocument"""
    id: int
    instructor_id: int
    file_path: str
    original_filename: Optional[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
