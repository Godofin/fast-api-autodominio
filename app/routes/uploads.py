from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uuid
from app.database import get_db
from app.models import User, InstructorProfile, InstructorDocument, DocumentType
from app.schemas import InstructorDocumentResponse

router = APIRouter(prefix="/uploads", tags=["Uploads"])

# Diretório para armazenar uploads
UPLOAD_DIR = Path("uploads")
PROFILE_PHOTOS_DIR = UPLOAD_DIR / "profile_photos"
DOCUMENTS_DIR = UPLOAD_DIR / "documents"

# Criar diretórios se não existirem
PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Extensões permitidas
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"}


def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    """Salvar arquivo de upload no disco"""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return str(destination)
    finally:
        upload_file.file.close()


@router.post("/profile-photo/{user_id}")
def upload_profile_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload de foto de perfil do usuário"""
    # Verificar se usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Validar extensão do arquivo
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão de arquivo não permitida. Use: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Gerar nome único para o arquivo
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = PROFILE_PHOTOS_DIR / unique_filename
    
    # Deletar foto antiga se existir
    if user.profile_photo and os.path.exists(user.profile_photo):
        try:
            os.remove(user.profile_photo)
        except:
            pass
    
    # Salvar arquivo
    saved_path = save_upload_file(file, file_path)
    
    # Atualizar usuário
    user.profile_photo = saved_path
    db.commit()
    
    return {
        "message": "Foto de perfil enviada com sucesso",
        "user_id": user_id,
        "file_path": saved_path
    }


@router.post("/instructor-document/{instructor_profile_id}", response_model=InstructorDocumentResponse)
def upload_instructor_document(
    instructor_profile_id: int,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload de documento do instrutor"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == instructor_profile_id
    ).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    # Validar extensão do arquivo
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão de arquivo não permitida. Use: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
        )
    
    # Gerar nome único para o arquivo
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = DOCUMENTS_DIR / unique_filename
    
    # Salvar arquivo
    saved_path = save_upload_file(file, file_path)
    
    # Criar registro no banco
    document = InstructorDocument(
        instructor_id=instructor_profile_id,
        document_type=document_type,
        file_path=saved_path,
        original_filename=file.filename
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document


@router.get("/instructor-documents/{instructor_profile_id}", response_model=List[InstructorDocumentResponse])
def list_instructor_documents(instructor_profile_id: int, db: Session = Depends(get_db)):
    """Listar documentos de um instrutor"""
    # Verificar se instrutor existe
    instructor = db.query(InstructorProfile).filter(
        InstructorProfile.id == instructor_profile_id
    ).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de instrutor não encontrado"
        )
    
    documents = db.query(InstructorDocument).filter(
        InstructorDocument.instructor_id == instructor_profile_id
    ).all()
    return documents


@router.delete("/instructor-document/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor_document(document_id: int, db: Session = Depends(get_db)):
    """Deletar documento do instrutor"""
    document = db.query(InstructorDocument).filter(InstructorDocument.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Deletar arquivo do disco
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except:
            pass
    
    # Deletar registro do banco
    db.delete(document)
    db.commit()
    return None


@router.get("/info")
def get_upload_info():
    """Obter informações sobre uploads permitidos"""
    return {
        "profile_photos": {
            "allowed_extensions": list(ALLOWED_IMAGE_EXTENSIONS),
            "max_size": "10MB (recomendado)",
            "directory": str(PROFILE_PHOTOS_DIR)
        },
        "documents": {
            "allowed_extensions": list(ALLOWED_DOCUMENT_EXTENSIONS),
            "max_size": "20MB (recomendado)",
            "directory": str(DOCUMENTS_DIR),
            "document_types": [dt.value for dt in DocumentType]
        }
    }
