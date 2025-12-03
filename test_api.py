"""
Script de teste para a API AutoDomínio
Execute este script após iniciar a API para testar todos os endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Função auxiliar para imprimir respostas"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def test_api():
    """Função principal de teste"""
    
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES DA API AUTODOMÍNIO")
    print("="*60 + "\n")
    
    # 1. Testar endpoint raiz
    print("1️⃣ Testando endpoint raiz...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    
    # 2. Testar health check
    print("2️⃣ Testando health check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", response)
    
    # 3. Criar um aluno
    print("3️⃣ Criando um aluno...")
    student_data = {
        "name": "João Silva",
        "email": "joao@email.com",
        "password": "senha123",
        "role": "student",
        "phone": "11999999999"
    }
    response = requests.post(f"{BASE_URL}/users/", json=student_data)
    print_response("POST /users/ (Aluno)", response)
    student_id = response.json().get("id") if response.status_code == 201 else None
    
    # 4. Criar um instrutor
    print("4️⃣ Criando um instrutor...")
    instructor_data = {
        "name": "Maria Santos",
        "email": "maria@email.com",
        "password": "senha123",
        "role": "instructor",
        "phone": "11988888888"
    }
    response = requests.post(f"{BASE_URL}/users/", json=instructor_data)
    print_response("POST /users/ (Instrutor)", response)
    instructor_user_id = response.json().get("id") if response.status_code == 201 else None
    
    # 5. Criar outro instrutor
    print("5️⃣ Criando outro instrutor...")
    instructor_data_2 = {
        "name": "Carlos Oliveira",
        "email": "carlos@email.com",
        "password": "senha123",
        "role": "instructor",
        "phone": "11977777777"
    }
    response = requests.post(f"{BASE_URL}/users/", json=instructor_data_2)
    print_response("POST /users/ (Instrutor 2)", response)
    instructor_user_id_2 = response.json().get("id") if response.status_code == 201 else None
    
    # 6. Listar usuários
    print("6️⃣ Listando todos os usuários...")
    response = requests.get(f"{BASE_URL}/users/")
    print_response("GET /users/", response)
    
    # 7. Criar perfil do instrutor 1
    if instructor_user_id:
        print("7️⃣ Criando perfil do instrutor 1...")
        profile_data = {
            "user_id": instructor_user_id,
            "bio": "Instrutora com 10 anos de experiência, especialista em perda de medo",
            "credential_number": "DETRAN-SP-12345",
            "hourly_rate": 80.00,
            "car_model": "Gol G7",
            "transmission": "manual",
            "city": "São Paulo"
        }
        response = requests.post(f"{BASE_URL}/instructor-profiles/", json=profile_data)
        print_response("POST /instructor-profiles/", response)
        instructor_profile_id = response.json().get("id") if response.status_code == 201 else None
    
    # 8. Criar perfil do instrutor 2
    if instructor_user_id_2:
        print("8️⃣ Criando perfil do instrutor 2...")
        profile_data_2 = {
            "user_id": instructor_user_id_2,
            "bio": "Instrutor especializado em câmbio automático e trânsito urbano",
            "credential_number": "DETRAN-SP-67890",
            "hourly_rate": 95.00,
            "car_model": "Onix Plus",
            "transmission": "automatic",
            "city": "São Paulo"
        }
        response = requests.post(f"{BASE_URL}/instructor-profiles/", json=profile_data_2)
        print_response("POST /instructor-profiles/ (Instrutor 2)", response)
        instructor_profile_id_2 = response.json().get("id") if response.status_code == 201 else None
    
    # 9. Buscar instrutores com filtros
    print("9️⃣ Buscando instrutores em São Paulo com câmbio manual...")
    response = requests.get(f"{BASE_URL}/instructor-profiles/?city=São Paulo&transmission=manual")
    print_response("GET /instructor-profiles/ (com filtros)", response)
    
    # 10. Criar disponibilidade para instrutor 1
    if instructor_profile_id:
        print("🔟 Criando disponibilidade do instrutor 1 (Segunda-feira)...")
        availability_data = {
            "instructor_id": instructor_profile_id,
            "day_of_week": 1,  # Segunda
            "start_time": "08:00:00",
            "end_time": "12:00:00",
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/instructor-availability/", json=availability_data)
        print_response("POST /instructor-availability/", response)
        
        print("1️⃣1️⃣ Criando disponibilidade do instrutor 1 (Quarta-feira)...")
        availability_data_2 = {
            "instructor_id": instructor_profile_id,
            "day_of_week": 3,  # Quarta
            "start_time": "14:00:00",
            "end_time": "18:00:00",
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/instructor-availability/", json=availability_data_2)
        print_response("POST /instructor-availability/ (Quarta)", response)
    
    # 11. Listar disponibilidades do instrutor
    if instructor_profile_id:
        print("1️⃣2️⃣ Listando disponibilidades do instrutor 1...")
        response = requests.get(f"{BASE_URL}/instructor-availability/instructor/{instructor_profile_id}")
        print_response(f"GET /instructor-availability/instructor/{instructor_profile_id}", response)
    
    # 12. Criar agendamento
    if student_id and instructor_user_id:
        print("1️⃣3️⃣ Criando agendamento...")
        # Data de amanhã às 14h
        tomorrow = datetime.now() + timedelta(days=1)
        start_date = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(hours=1)
        
        appointment_data = {
            "student_id": student_id,
            "instructor_id": instructor_user_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "location_pickup": "Av. Paulista, 1000 - São Paulo",
            "notes": "Tenho medo de dirigir em ladeiras e preciso praticar baliza"
        }
        response = requests.post(f"{BASE_URL}/appointments/", json=appointment_data)
        print_response("POST /appointments/", response)
        appointment_id = response.json().get("id") if response.status_code == 201 else None
    
    # 13. Listar agendamentos
    print("1️⃣4️⃣ Listando todos os agendamentos...")
    response = requests.get(f"{BASE_URL}/appointments/")
    print_response("GET /appointments/", response)
    
    # 14. Atualizar status do agendamento
    if appointment_id:
        print("1️⃣5️⃣ Atualizando status do agendamento para 'confirmed'...")
        response = requests.patch(f"{BASE_URL}/appointments/{appointment_id}/status?new_status=confirmed")
        print_response(f"PATCH /appointments/{appointment_id}/status", response)
    
    # 15. Criar exceção na agenda (dia bloqueado)
    if instructor_profile_id:
        print("1️⃣6️⃣ Bloqueando dia na agenda do instrutor...")
        next_week = datetime.now() + timedelta(days=7)
        time_off_data = {
            "instructor_id": instructor_profile_id,
            "date": next_week.date().isoformat(),
            "reason": "Férias"
        }
        response = requests.post(f"{BASE_URL}/instructor-time-off/", json=time_off_data)
        print_response("POST /instructor-time-off/", response)
    
    # 16. Listar exceções do instrutor
    if instructor_profile_id:
        print("1️⃣7️⃣ Listando exceções de agenda do instrutor...")
        response = requests.get(f"{BASE_URL}/instructor-time-off/instructor/{instructor_profile_id}")
        print_response(f"GET /instructor-time-off/instructor/{instructor_profile_id}", response)
    
    # 17. Buscar agendamentos por aluno
    if student_id:
        print("1️⃣8️⃣ Buscando agendamentos do aluno...")
        response = requests.get(f"{BASE_URL}/appointments/?student_id={student_id}")
        print_response(f"GET /appointments/?student_id={student_id}", response)
    
    # 18. Buscar agendamentos por instrutor
    if instructor_user_id:
        print("1️⃣9️⃣ Buscando agendamentos do instrutor...")
        response = requests.get(f"{BASE_URL}/appointments/?instructor_id={instructor_user_id}")
        print_response(f"GET /appointments/?instructor_id={instructor_user_id}", response)
    
    # 19. Atualizar usuário
    if student_id:
        print("2️⃣0️⃣ Atualizando telefone do aluno...")
        update_data = {
            "phone": "11955555555"
        }
        response = requests.put(f"{BASE_URL}/users/{student_id}", json=update_data)
        print_response(f"PUT /users/{student_id}", response)
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*60 + "\n")
    print("💡 Dicas:")
    print("   - Acesse http://localhost:8000/docs para ver a documentação interativa")
    print("   - Acesse http://localhost:8000/redoc para ver a documentação alternativa")
    print("   - O banco de dados SQLite foi criado em: autodominio.db")
    print("\n")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API!")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        print("   Execute: python main.py")
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
