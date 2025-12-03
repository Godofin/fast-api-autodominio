from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class DocumentType(str, enum.Enum):
    """Enum para tipo de documento"""
    CNH = "cnh"  # Carteira Nacional de Habilitação
    CREDENTIAL = "credential"  # Credencial de Instrutor
    CERTIFICATE = "certificate"  # Certificado do curso de instrutor
    RG = "rg"  # Registro Geral
    CPF = "cpf"  # Cadastro de Pessoa Física
    PROOF_OF_ADDRESS = "proof_of_address"  # Comprovante de residência
    VEHICLE_DOCUMENT = "vehicle_document"  # Documento do veículo
    OTHER = "other"  # Outros documentos


class InstructorDocument(Base):
    """Modelo de Documentos do Instrutor"""
    __tablename__ = "instructor_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, ForeignKey("instructor_profiles.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    file_path = Column(String(500), nullable=False)  # Caminho do arquivo
    original_filename = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    instructor = relationship("InstructorProfile", back_populates="documents")
