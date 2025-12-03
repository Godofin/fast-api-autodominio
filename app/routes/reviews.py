from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Review, Appointment, User, UserRole, AppointmentStatus
from app.schemas import ReviewCreate, ReviewUpdate, ReviewResponse, InstructorRatingStats

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Criar uma nova avaliação"""
    # Verificar se o agendamento existe e está completo
    appointment = db.query(Appointment).filter(Appointment.id == review.appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    if appointment.status != AppointmentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Só é possível avaliar agendamentos concluídos"
        )
    
    # Verificar se já existe avaliação para este agendamento
    existing_review = db.query(Review).filter(Review.appointment_id == review.appointment_id).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este agendamento já foi avaliado"
        )
    
    # Criar avaliação
    db_review = Review(
        appointment_id=review.appointment_id,
        student_id=appointment.student_id,
        instructor_id=review.instructor_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/instructor/{instructor_id}", response_model=List[ReviewResponse])
def list_instructor_reviews(instructor_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar avaliações de um instrutor específico"""
    # Verificar se instrutor existe
    instructor = db.query(User).filter(User.id == instructor_id, User.role == UserRole.INSTRUCTOR).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    reviews = db.query(Review).filter(
        Review.instructor_id == instructor_id
    ).offset(skip).limit(limit).all()
    return reviews


@router.get("/instructor/{instructor_id}/stats", response_model=InstructorRatingStats)
def get_instructor_rating_stats(instructor_id: int, db: Session = Depends(get_db)):
    """Obter estatísticas de avaliação de um instrutor"""
    # Verificar se instrutor existe
    instructor = db.query(User).filter(User.id == instructor_id, User.role == UserRole.INSTRUCTOR).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrutor não encontrado"
        )
    
    # Calcular média e total
    stats = db.query(
        func.avg(Review.rating).label('average'),
        func.count(Review.id).label('total')
    ).filter(Review.instructor_id == instructor_id).first()
    
    average_rating = float(stats.average) if stats.average else 0.0
    total_reviews = stats.total
    
    # Calcular distribuição de ratings
    rating_distribution = {}
    for rating in range(1, 6):
        count = db.query(Review).filter(
            Review.instructor_id == instructor_id,
            Review.rating == rating
        ).count()
        rating_distribution[rating] = count
    
    return InstructorRatingStats(
        instructor_id=instructor_id,
        average_rating=round(average_rating, 2),
        total_reviews=total_reviews,
        rating_distribution=rating_distribution
    )


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Obter uma avaliação específica"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    """Atualizar uma avaliação"""
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )
    
    # Atualizar campos fornecidos
    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Deletar uma avaliação"""
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )
    
    db.delete(db_review)
    db.commit()
    return None
