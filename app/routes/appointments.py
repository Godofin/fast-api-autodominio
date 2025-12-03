from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Appointment, User, UserRole, AppointmentStatus
from app.schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """Criar um novo agendamento"""
    # Verificar se aluno existe e é do tipo student
    student = db.query(User).filter(User.id == appointment.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    if student.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não é um aluno"
        )
    
    # Verificar se instrutor existe e é do tipo instructor
    instructor = db.query(User).filter(User.id == appointment.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    if instructor.role != UserRole.INSTRUCTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não é um instrutor"
        )
    
    # Criar agendamento
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[int] = Query(None, description="Filtrar por ID do aluno"),
    instructor_id: Optional[int] = Query(None, description="Filtrar por ID do instrutor"),
    status_filter: Optional[AppointmentStatus] = Query(None, alias="status", description="Filtrar por status"),
    db: Session = Depends(get_db)
):
    """Listar agendamentos com filtros opcionais"""
    query = db.query(Appointment)
    
    if student_id:
        query = query.filter(Appointment.student_id == student_id)
    if instructor_id:
        query = query.filter(Appointment.instructor_id == instructor_id)
    if status_filter:
        query = query.filter(Appointment.status == status_filter)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Obter um agendamento específico"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar um agendamento"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    # Atualizar campos fornecidos
    update_data = appointment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Deletar um agendamento"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    db.delete(db_appointment)
    db.commit()
    return None


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    new_status: AppointmentStatus,
    db: Session = Depends(get_db)
):
    """Atualizar apenas o status de um agendamento"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    db_appointment.status = new_status
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
