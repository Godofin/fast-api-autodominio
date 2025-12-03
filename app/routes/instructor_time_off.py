from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import InstructorTimeOff, InstructorProfile
from app.schemas import InstructorTimeOffCreate, InstructorTimeOffUpdate, InstructorTimeOffResponse

router = APIRouter(prefix="/instructor-time-off", tags=["Instructor Time Off"])


@router.post("/", response_model=InstructorTimeOffResponse, status_code=status.HTTP_201_CREATED)
def create_time_off(time_off: InstructorTimeOffCreate, db: Session = Depends(get_db)):
    """Criar nova exceção na agenda (dia bloqueado)"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == time_off.instructor_id
    ).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    # Criar exceção
    db_time_off = InstructorTimeOff(**time_off.model_dump())
    db.add(db_time_off)
    db.commit()
    db.refresh(db_time_off)
    return db_time_off


@router.get("/instructor/{instructor_id}", response_model=List[InstructorTimeOffResponse])
def list_instructor_time_off(instructor_id: int, db: Session = Depends(get_db)):
    """Listar exceções de agenda de um instrutor específico"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(InstructorProfile.id == instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    time_offs = db.query(InstructorTimeOff).filter(
        InstructorTimeOff.instructor_id == instructor_id
    ).all()
    return time_offs


@router.get("/{time_off_id}", response_model=InstructorTimeOffResponse)
def get_time_off(time_off_id: int, db: Session = Depends(get_db)):
    """Obter uma exceção específica"""
    time_off = db.query(InstructorTimeOff).filter(InstructorTimeOff.id == time_off_id).first()
    if not time_off:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exceção de agenda não encontrada"
        )
    return time_off


@router.put("/{time_off_id}", response_model=InstructorTimeOffResponse)
def update_time_off(
    time_off_id: int,
    time_off_update: InstructorTimeOffUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar uma exceção de agenda"""
    db_time_off = db.query(InstructorTimeOff).filter(InstructorTimeOff.id == time_off_id).first()
    if not db_time_off:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exceção de agenda não encontrada"
        )
    
    # Atualizar campos fornecidos
    update_data = time_off_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_time_off, field, value)
    
    db.commit()
    db.refresh(db_time_off)
    return db_time_off


@router.delete("/{time_off_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_off(time_off_id: int, db: Session = Depends(get_db)):
    """Deletar uma exceção de agenda"""
    db_time_off = db.query(InstructorTimeOff).filter(InstructorTimeOff.id == time_off_id).first()
    if not db_time_off:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exceção de agenda não encontrada"
        )
    
    db.delete(db_time_off)
    db.commit()
    return None
