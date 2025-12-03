from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import InstructorProfile, User, UserRole
from app.schemas import InstructorProfileCreate, InstructorProfileUpdate, InstructorProfileResponse

router = APIRouter(prefix="/instructor-profiles", tags=["Instructor Profiles"])


@router.post("/", response_model=InstructorProfileResponse, status_code=status.HTTP_201_CREATED)
def create_instructor_profile(profile: InstructorProfileCreate, db: Session = Depends(get_db)):
    """Criar um novo perfil de instrutor"""
    # Verificar se usuário existe e é instrutor
    user = db.query(User).filter(User.id == profile.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    if user.role != UserRole.INSTRUCTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não é um instrutor"
        )
    
    # Verificar se já existe perfil para este usuário
    existing_profile = db.query(InstructorProfile).filter(
        InstructorProfile.user_id == profile.user_id
    ).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil de instrutor já existe para este usuário"
        )
    
    # Verificar se credential_number já existe
    existing_credential = db.query(InstructorProfile).filter(
        InstructorProfile.credential_number == profile.credential_number
    ).first()
    if existing_credential:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de credencial já cadastrado"
        )
    
    # Criar perfil
    db_profile = InstructorProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/", response_model=List[InstructorProfileResponse])
def list_instructor_profiles(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    transmission: Optional[str] = Query(None, description="Filtrar por tipo de transmissão"),
    min_rate: Optional[float] = Query(None, description="Preço mínimo por hora"),
    max_rate: Optional[float] = Query(None, description="Preço máximo por hora"),
    db: Session = Depends(get_db)
):
    """Listar perfis de instrutores com filtros opcionais"""
    query = db.query(InstructorProfile)
    
    if city:
        query = query.filter(InstructorProfile.city.ilike(f"%{city}%"))
    if transmission:
        query = query.filter(InstructorProfile.transmission == transmission)
    if min_rate is not None:
        query = query.filter(InstructorProfile.hourly_rate >= min_rate)
    if max_rate is not None:
        query = query.filter(InstructorProfile.hourly_rate <= max_rate)
    
    profiles = query.offset(skip).limit(limit).all()
    return profiles


@router.get("/{profile_id}", response_model=InstructorProfileResponse)
def get_instructor_profile(profile_id: int, db: Session = Depends(get_db)):
    """Obter um perfil de instrutor específico"""
    profile = db.query(InstructorProfile).filter(InstructorProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    return profile


@router.get("/user/{user_id}", response_model=InstructorProfileResponse)
def get_instructor_profile_by_user(user_id: int, db: Session = Depends(get_db)):
    """Obter perfil de instrutor por ID do usuário"""
    profile = db.query(InstructorProfile).filter(InstructorProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado para este usuário"
        )
    return profile


@router.put("/{profile_id}", response_model=InstructorProfileResponse)
def update_instructor_profile(
    profile_id: int,
    profile_update: InstructorProfileUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar um perfil de instrutor"""
    db_profile = db.query(InstructorProfile).filter(InstructorProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    # Atualizar campos fornecidos
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor_profile(profile_id: int, db: Session = Depends(get_db)):
    """Deletar um perfil de instrutor"""
    db_profile = db.query(InstructorProfile).filter(InstructorProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    db.delete(db_profile)
    db.commit()
    return None
