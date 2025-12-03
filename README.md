# AutoDomínio API

API REST para conectar instrutores de trânsito credenciados a alunos que buscam aulas avulsas de aperfeiçoamento ou perda de medo.

## 📍 Funcionalidades

### Funcionalidades Básicas
- **Gestão de Usuários**: Cadastro de alunos, instrutores e administradores
- **Perfis de Instrutores**: Informações detalhadas sobre credenciais, veículo e preços
- **Disponibilidade**: Gestão de agenda semanal dos instrutores
- **Agendamentos**: Sistema completo de marcação e gestão de aulas
- **Exceções de Agenda**: Bloqueio de datas específicas para instrutores
- **Busca Avançada**: Filtros por localização, tipo de câmbio e preço

### 🆕 Novas Funcionalidades (v2.0)
- **⭐ Sistema de Avaliações**: Alunos podem avaliar instrutores (1-5 estrelas)
- **✅ Aprovação de Instrutores**: Sistema de aprovação antes de dar aulas
- **📸 Upload de Fotos**: Fotos de perfil para usuários
- **📄 Upload de Documentos**: Instrutores podem enviar CNH, credenciais, etc.
- **📊 Estatísticas**: Média de avaliações e estatísticas de aprovação

## 🚀 Como Executar no Windows

### Pré-requisitos

- Python 3.11 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

Abra o **Prompt de Comando** ou **PowerShell** na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### Passo 2: Executar a API

```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

### Passo 3: Acessar a Documentação Interativa

Abra seu navegador e acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
autodominio/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py          # Configuração do banco de dados
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # Modelo de Usuário
│   │   ├── instructor_profile.py  # Modelo de Perfil do Instrutor
│   │   ├── instructor_availability.py  # Modelo de Disponibilidade
│   │   ├── appointment.py         # Modelo de Agendamento
│   │   └── instructor_time_off.py # Modelo de Exceções
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                # Schemas Pydantic para User
│   │   ├── instructor_profile.py  # Schemas para InstructorProfile
│   │   ├── instructor_availability.py
│   │   ├── appointment.py
│   │   └── instructor_time_off.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py               # Rotas de usuários
│   │   ├── instructor_profiles.py # Rotas de perfis
│   │   ├── instructor_availability.py
│   │   ├── appointments.py
│   │   └── instructor_time_off.py
│   ├── __init__.py
│   └── config.py                  # Configurações da aplicação
├── tests/                         # Pasta para testes
├── .env                           # Variáveis de ambiente
├── main.py                        # Arquivo principal da aplicação
├── requirements.txt               # Dependências do projeto
└── README.md                      # Este arquivo
```

## 🗄️ Banco de Dados

A API utiliza **SQLite** por padrão para facilitar testes locais. O arquivo do banco de dados (`autodominio.db`) será criado automaticamente na primeira execução.

### Tabelas

1. **users** - Usuários do sistema (alunos, instrutores, admins)
2. **instructor_profiles** - Perfis detalhados dos instrutores
3. **instructor_availability** - Disponibilidade semanal dos instrutores
4. **appointments** - Agendamentos de aulas
5. **instructor_time_off** - Exceções na agenda (dias bloqueados)

## 📚 Endpoints da API

### Usuários (`/users`)

- `POST /users/` - Criar novo usuário
- `GET /users/` - Listar todos os usuários
- `GET /users/{user_id}` - Obter usuário específico
- `PUT /users/{user_id}` - Atualizar usuário
- `DELETE /users/{user_id}` - Deletar usuário

### Perfis de Instrutores (`/instructor-profiles`)

- `POST /instructor-profiles/` - Criar perfil de instrutor
- `GET /instructor-profiles/` - Listar perfis (com filtros)
- `GET /instructor-profiles/{profile_id}` - Obter perfil específico
- `GET /instructor-profiles/user/{user_id}` - Obter perfil por ID do usuário
- `PUT /instructor-profiles/{profile_id}` - Atualizar perfil
- `DELETE /instructor-profiles/{profile_id}` - Deletar perfil

**Filtros disponíveis:**
- `city` - Filtrar por cidade
- `transmission` - Filtrar por tipo de transmissão (manual/automatic)
- `min_rate` - Preço mínimo por hora
- `max_rate` - Preço máximo por hora

### Disponibilidade (`/instructor-availability`)

- `POST /instructor-availability/` - Criar disponibilidade
- `GET /instructor-availability/instructor/{instructor_id}` - Listar disponibilidades do instrutor
- `GET /instructor-availability/{availability_id}` - Obter disponibilidade específica
- `PUT /instructor-availability/{availability_id}` - Atualizar disponibilidade
- `DELETE /instructor-availability/{availability_id}` - Deletar disponibilidade

### Agendamentos (`/appointments`)

- `POST /appointments/` - Criar agendamento
- `GET /appointments/` - Listar agendamentos (com filtros)
- `GET /appointments/{appointment_id}` - Obter agendamento específico
- `PUT /appointments/{appointment_id}` - Atualizar agendamento
- `PATCH /appointments/{appointment_id}/status` - Atualizar apenas o status
- `DELETE /appointments/{appointment_id}` - Deletar agendamento

**Filtros disponíveis:**
- `student_id` - Filtrar por ID do aluno
- `instructor_id` - Filtrar por ID do instrutor
- `status` - Filtrar por status (pending/confirmed/cancelled/completed)

### Exceções de Agenda (`/instructor-time-off`)

- `POST /instructor-time-off/` - Criar exceção (bloquear dia)
- `GET /instructor-time-off/instructor/{instructor_id}` - Listar exceções do instrutor
- `GET /instructor-time-off/{time_off_id}` - Obter exceção específica
- `PUT /instructor-time-off/{time_off_id}` - Atualizar exceção
- `DELETE /instructor-time-off/{time_off_id}` - Deletar exceção

## 🧪 Exemplos de Uso

### 1. Criar um Aluno

```bash
POST http://localhost:8000/users/
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@email.com",
  "password": "senha123",
  "role": "student",
  "phone": "11999999999"
}
```

### 2. Criar um Instrutor

```bash
POST http://localhost:8000/users/
Content-Type: application/json

{
  "name": "Maria Santos",
  "email": "maria@email.com",
  "password": "senha123",
  "role": "instructor",
  "phone": "11988888888"
}
```

### 3. Criar Perfil do Instrutor

```bash
POST http://localhost:8000/instructor-profiles/
Content-Type: application/json

{
  "user_id": 2,
  "bio": "Instrutora com 10 anos de experiência, especialista em perda de medo",
  "credential_number": "DETRAN-SP-12345",
  "hourly_rate": 80.00,
  "car_model": "Gol G7",
  "transmission": "manual",
  "city": "São Paulo"
}
```

### 4. Definir Disponibilidade do Instrutor

```bash
POST http://localhost:8000/instructor-availability/
Content-Type: application/json

{
  "instructor_id": 1,
  "day_of_week": 1,
  "start_time": "08:00:00",
  "end_time": "12:00:00",
  "is_active": true
}
```

### 5. Buscar Instrutores

```bash
GET http://localhost:8000/instructor-profiles/?city=São Paulo&transmission=manual&max_rate=100
```

### 6. Criar Agendamento

```bash
POST http://localhost:8000/appointments/
Content-Type: application/json

{
  "student_id": 1,
  "instructor_id": 2,
  "start_date": "2024-01-15T14:00:00",
  "end_date": "2024-01-15T15:00:00",
  "location_pickup": "Av. Paulista, 1000",
  "notes": "Tenho medo de dirigir em ladeiras"
}
```

### 7. Atualizar Status do Agendamento

```bash
PATCH http://localhost:8000/appointments/1/status?new_status=confirmed
```

### 8. Bloquear Dia na Agenda

```bash
POST http://localhost:8000/instructor-time-off/
Content-Type: application/json

{
  "instructor_id": 1,
  "date": "2024-01-20",
  "reason": "Férias"
}
```

## 🔧 Configurações

As configurações podem ser alteradas no arquivo `.env`:

```env
DATABASE_URL=sqlite:///./autodominio.db
APP_NAME=AutoDominio API
DEBUG=True
```

## 📝 Tipos de Dados

### UserRole (Tipo de Usuário)
- `student` - Aluno
- `instructor` - Instrutor
- `admin` - Administrador

### TransmissionType (Tipo de Transmissão)
- `manual` - Câmbio manual
- `automatic` - Câmbio automático

### AppointmentStatus (Status do Agendamento)
- `pending` - Pendente
- `confirmed` - Confirmado
- `cancelled` - Cancelado
- `completed` - Concluído

### day_of_week (Dia da Semana)
- `0` - Domingo
- `1` - Segunda-feira
- `2` - Terça-feira
- `3` - Quarta-feira
- `4` - Quinta-feira
- `5` - Sexta-feira
- `6` - Sábado

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **SQLite** - Banco de dados (para desenvolvimento)

## 📌 Observações

- Esta versão **não utiliza autenticação JWT** para facilitar testes locais
- As senhas são armazenadas com hash simples (em produção, usar bcrypt)
- O CORS está configurado para aceitar todas as origens (ajustar em produção)
- Para produção, considere migrar para PostgreSQL ou MySQL

## 🚀 Próximos Passos (Produção)

1. Implementar autenticação JWT
2. Adicionar bcrypt para hash de senhas
3. Migrar para banco de dados PostgreSQL/MySQL
4. Implementar sistema de pagamentos
5. Adicionar validação de conflitos de horários
6. Implementar notificações (email/SMS)
7. Adicionar sistema de avaliações
8. Implementar upload de fotos de perfil e documentos

## 📧 Suporte

Para dúvidas ou sugestões, entre em contato através do repositório do projeto.

---

**AutoDomínio** - Conectando instrutores e alunos de forma simples e eficiente! 🚗
