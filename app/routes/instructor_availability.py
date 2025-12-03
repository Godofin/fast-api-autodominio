from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import InstructorAvailability, InstructorProfile
from app.schemas import InstructorAvailabilityCreate, InstructorAvailabilityUpdate, InstructorAvailabilityResponse

router = APIRouter(prefix="/instructor-availability", tags=["Instructor Availability"])


@router.post("/", response_model=InstructorAvailabilityResponse, status_code=status.HTTP_201_CREATED)
def create_availability(availability: InstructorAvailabilityCreate, db: Session = Depends(get_db)):
    """Criar nova disponibilidade para instrutor"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == availability.instructor_id
    ).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    # Criar disponibilidade
    db_availability = InstructorAvailability(**availability.model_dump())
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability


@router.get("/instructor/{instructor_id}", response_model=List[InstructorAvailabilityResponse])
def list_instructor_availability(instructor_id: int, db: Session = Depends(get_db)):
    """Listar disponibilidades de um instrutor específico"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(InstructorProfile.id == instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    availabilities = db.query(InstructorAvailability).filter(
        InstructorAvailability.instructor_id == instructor_id
    ).all()
    return availabilities


@router.get("/{availability_id}", response_model=InstructorAvailabilityResponse)
def get_availability(availability_id: int, db: Session = Depends(get_db)):
    """Obter uma disponibilidade específica"""
    availability = db.query(InstructorAvailability).filter(
        InstructorAvailability.id == availability_id
    ).first()
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disponibilidade não encontrada"
        )
    return availability


@router.put("/{availability_id}", response_model=InstructorAvailabilityResponse)
def update_availability(
    availability_id: int,
    availability_update: InstructorAvailabilityUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar uma disponibilidade"""
    db_availability = db.query(InstructorAvailability).filter(
        InstructorAvailability.id == availability_id
    ).first()
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disponibilidade não encontrada"
        )
    
    # Atualizar campos fornecidos
    update_data = availability_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_availability, field, value)
    
    db.commit()
    db.refresh(db_availability)
    return db_availability


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    """Deletar uma disponibilidade"""
    db_availability = db.query(InstructorAvailability).filter(
        InstructorAvailability.id == availability_id
    ).first()
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disponibilidade não encontrada"
        )
    
    db.delete(db_availability)
    db.commit()
    return None
