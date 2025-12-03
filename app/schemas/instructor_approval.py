from pydantic import BaseModel, Field
from typing import Optional
from app.models.instructor_profile import ApprovalStatus


class InstructorApprovalUpdate(BaseModel):
    """Schema para atualizar status de aprovação do instrutor"""
    approval_status: ApprovalStatus
    rejection_reason: Optional[str] = Field(None, description="Motivo da rejeição (obrigatório se status for 'rejected')")
