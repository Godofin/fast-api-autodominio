from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import InstructorProfile, ApprovalStatus
from app.schemas import InstructorProfileResponse, InstructorApprovalUpdate

router = APIRouter(prefix="/instructor-approval", tags=["Instructor Approval"])


@router.get("/pending", response_model=List[InstructorProfileResponse])
def list_pending_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar instrutores aguardando aprovação"""
    instructors = db.query(InstructorProfile).filter(
        InstructorProfile.approval_status == ApprovalStatus.PENDING
    ).offset(skip).limit(limit).all()
    return instructors


@router.get("/under-review", response_model=List[InstructorProfileResponse])
def list_under_review_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar instrutores em análise"""
    instructors = db.query(InstructorProfile).filter(
        InstructorProfile.approval_status == ApprovalStatus.UNDER_REVIEW
    ).offset(skip).limit(limit).all()
    return instructors


@router.get("/approved", response_model=List[InstructorProfileResponse])
def list_approved_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar instrutores aprovados"""
    instructors = db.query(InstructorProfile).filter(
        InstructorProfile.approval_status == ApprovalStatus.APPROVED
    ).offset(skip).limit(limit).all()
    return instructors


@router.get("/rejected", response_model=List[InstructorProfileResponse])
def list_rejected_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar instrutores rejeitados"""
    instructors = db.query(InstructorProfile).filter(
        InstructorProfile.approval_status == ApprovalStatus.REJECTED
    ).offset(skip).limit(limit).all()
    return instructors


@router.patch("/{instructor_profile_id}/status", response_model=InstructorProfileResponse)
def update_instructor_approval_status(
    instructor_profile_id: int,
    approval_update: InstructorApprovalUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar status de aprovação de um instrutor"""
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == instructor_profile_id
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    # Validar que rejection_reason é obrigatório se status for rejected
    if approval_update.approval_status == ApprovalStatus.REJECTED:
        if not approval_update.rejection_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Motivo da rejeição é obrigatório quando o status é 'rejected'"
            )
    
    # Atualizar status
    instructor.approval_status = approval_update.approval_status
    instructor.rejection_reason = approval_update.rejection_reason
    
    # Se aprovado ou rejeitado, registrar data
    if approval_update.approval_status in [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED]:
        instructor.approval_date = datetime.utcnow()
    
    db.commit()
    db.refresh(instructor)
    return instructor


@router.patch("/{instructor_profile_id}/set-under-review", response_model=InstructorProfileResponse)
def set_instructor_under_review(instructor_profile_id: int, db: Session = Depends(get_db)):
    """Marcar instrutor como 'em análise'"""
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == instructor_profile_id
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    instructor.approval_status = ApprovalStatus.UNDER_REVIEW
    db.commit()
    db.refresh(instructor)
    return instructor


@router.get("/stats")
def get_approval_stats(db: Session = Depends(get_db)):
    """Obter estatísticas de aprovação de instrutores"""
    stats = {}
    for status_value in ApprovalStatus:
        count = db.query(InstructorProfile).filter(
            InstructorProfile.approval_status == status_value
        ).count()
        stats[status_value.value] = count
    
    return {
        "approval_stats": stats,
        "total_instructors": sum(stats.values())
    }
