from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import (
    users_router,
    instructor_profiles_router,
    instructor_availability_router,
    appointments_router,
    instructor_time_off_router
)
from app.config import settings

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para conectar instrutores de trânsito a alunos",
    version="1.0.0",
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(users_router)
app.include_router(instructor_profiles_router)
app.include_router(instructor_availability_router)
app.include_router(appointments_router)
app.include_router(instructor_time_off_router)


@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "Bem-vindo à API AutoDomínio",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
