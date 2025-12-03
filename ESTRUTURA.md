# 📂 Estrutura do Projeto AutoDomínio

## Visão Geral da Arquitetura

A API AutoDomínio segue uma arquitetura em camadas bem definida, separando responsabilidades e facilitando manutenção:

```
autodominio/
│
├── app/                          # Código principal da aplicação
│   ├── database/                 # Camada de banco de dados
│   │   ├── __init__.py
│   │   └── connection.py         # Configuração SQLAlchemy + sessão
│   │
│   ├── models/                   # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py               # Modelo User + enum UserRole
│   │   ├── instructor_profile.py # Modelo InstructorProfile + enum TransmissionType
│   │   ├── instructor_availability.py  # Modelo InstructorAvailability
│   │   ├── appointment.py        # Modelo Appointment + enum AppointmentStatus
│   │   └── instructor_time_off.py # Modelo InstructorTimeOff
│   │
│   ├── schemas/                  # Schemas Pydantic (validação)
│   │   ├── __init__.py
│   │   ├── user.py               # UserCreate, UserUpdate, UserResponse
│   │   ├── instructor_profile.py # Schemas para InstructorProfile
│   │   ├── instructor_availability.py
│   │   ├── appointment.py
│   │   └── instructor_time_off.py
│   │
│   ├── routes/                   # Endpoints da API (controllers)
│   │   ├── __init__.py
│   │   ├── users.py              # CRUD de usuários
│   │   ├── instructor_profiles.py # CRUD de perfis + busca com filtros
│   │   ├── instructor_availability.py # CRUD de disponibilidade
│   │   ├── appointments.py       # CRUD de agendamentos + filtros
│   │   └── instructor_time_off.py # CRUD de exceções de agenda
│   │
│   ├── __init__.py
│   └── config.py                 # Configurações (Settings)
│
├── tests/                        # Pasta para testes unitários (vazia)
│
├── main.py                       # Ponto de entrada da aplicação
├── test_api.py                   # Script de teste completo
├── requirements.txt              # Dependências Python
├── .env                          # Variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── README.md                     # Documentação principal
├── GUIA_WINDOWS.md              # Guia específico para Windows
└── ESTRUTURA.md                 # Este arquivo
```

## 🗄️ Camadas da Aplicação

### 1. **Database Layer** (`app/database/`)

Responsável pela conexão e configuração do banco de dados.

- **connection.py**: 
  - Cria o engine do SQLAlchemy
  - Define a SessionLocal para transações
  - Fornece a função `get_db()` como dependency injection

### 2. **Models Layer** (`app/models/`)

Define a estrutura das tabelas do banco de dados usando SQLAlchemy ORM.

| Arquivo | Tabela | Descrição |
|---------|--------|-----------|
| `user.py` | `users` | Usuários do sistema (alunos, instrutores, admins) |
| `instructor_profile.py` | `instructor_profiles` | Perfil detalhado dos instrutores |
| `instructor_availability.py` | `instructor_availability` | Disponibilidade semanal dos instrutores |
| `appointment.py` | `appointments` | Agendamentos de aulas |
| `instructor_time_off.py` | `instructor_time_off` | Exceções na agenda (dias bloqueados) |

**Relacionamentos:**
- User (1) → (0..1) InstructorProfile
- User (1) → (N) Appointments (como student)
- User (1) → (N) Appointments (como instructor)
- InstructorProfile (1) → (N) InstructorAvailability
- InstructorProfile (1) → (N) InstructorTimeOff

### 3. **Schemas Layer** (`app/schemas/`)

Define os contratos de entrada/saída da API usando Pydantic.

Para cada entidade, existem 3 schemas principais:

- **Create**: Dados necessários para criar um registro
- **Update**: Dados que podem ser atualizados (todos opcionais)
- **Response**: Dados retornados pela API (inclui ID e timestamps)

**Validações implementadas:**
- Tipos de dados corretos
- Tamanhos mínimos/máximos de strings
- Validação de email
- Validação de valores numéricos (ex: hourly_rate > 0)
- Validação de datas (end_date > start_date)

### 4. **Routes Layer** (`app/routes/`)

Define os endpoints HTTP e a lógica de negócio.

| Arquivo | Prefixo | Endpoints |
|---------|---------|-----------|
| `users.py` | `/users` | 5 endpoints (CRUD completo) |
| `instructor_profiles.py` | `/instructor-profiles` | 6 endpoints (CRUD + busca) |
| `instructor_availability.py` | `/instructor-availability` | 5 endpoints |
| `appointments.py` | `/appointments` | 6 endpoints (CRUD + status) |
| `instructor_time_off.py` | `/instructor-time-off` | 5 endpoints |

**Total: 27 endpoints**

### 5. **Configuration** (`app/config.py`)

Gerencia configurações da aplicação usando Pydantic Settings.

Variáveis carregadas do `.env`:
- `DATABASE_URL`: String de conexão do banco
- `APP_NAME`: Nome da aplicação
- `DEBUG`: Modo debug

## 🔄 Fluxo de uma Requisição

```
1. Cliente faz requisição HTTP
   ↓
2. FastAPI roteia para o endpoint correto (routes/)
   ↓
3. Pydantic valida os dados de entrada (schemas/)
   ↓
4. Endpoint executa lógica de negócio
   ↓
5. SQLAlchemy interage com o banco (models/)
   ↓
6. Dados são serializados (schemas/)
   ↓
7. Resposta JSON é retornada ao cliente
```

## 🎯 Padrões Utilizados

### Dependency Injection
```python
def endpoint(db: Session = Depends(get_db)):
    # db é injetado automaticamente
```

### Repository Pattern (implícito)
Cada rota acessa o banco através do ORM, seguindo o padrão repository.

### DTO (Data Transfer Objects)
Os schemas Pydantic funcionam como DTOs, separando a representação de dados da lógica de negócio.

### Separation of Concerns
- Models: O QUE armazenar
- Schemas: COMO validar
- Routes: QUANDO e POR QUE processar

## 🔐 Segurança (Atual vs Produção)

### Implementação Atual (Desenvolvimento)
- ❌ Sem autenticação JWT
- ❌ Senhas com hash simples
- ✅ CORS aberto (para testes)
- ✅ Validação de dados com Pydantic
- ✅ Proteção contra SQL Injection (ORM)

### Recomendações para Produção
- ✅ Implementar JWT
- ✅ Usar bcrypt para senhas
- ✅ Configurar CORS específico
- ✅ Rate limiting
- ✅ HTTPS obrigatório
- ✅ Validação de permissões por role

## 📊 Banco de Dados

### Tecnologia Atual
- **SQLite** (arquivo `autodominio.db`)
- Ideal para desenvolvimento e testes
- Zero configuração necessária

### Migração para Produção
Para migrar para PostgreSQL ou MySQL, basta alterar a `DATABASE_URL` no `.env`:

**PostgreSQL:**
```
DATABASE_URL=postgresql://user:password@localhost/autodominio
```

**MySQL:**
```
DATABASE_URL=mysql+pymysql://user:password@localhost/autodominio
```

E instalar o driver correspondente:
```bash
pip install psycopg2-binary  # PostgreSQL
# ou
pip install pymysql  # MySQL
```

## 🧪 Testes

### Estrutura de Testes (Futura)
```
tests/
├── test_users.py
├── test_instructor_profiles.py
├── test_appointments.py
└── conftest.py  # Fixtures compartilhadas
```

### Script de Teste Atual
O arquivo `test_api.py` testa todos os endpoints de forma integrada.

## 📦 Dependências

| Pacote | Versão | Propósito |
|--------|--------|-----------|
| fastapi | 0.104.1 | Framework web |
| uvicorn | 0.24.0 | Servidor ASGI |
| sqlalchemy | 2.0.23 | ORM |
| pydantic | 2.5.0 | Validação de dados |
| pydantic-settings | 2.1.0 | Gerenciamento de configurações |
| python-dotenv | 1.0.0 | Carregar variáveis .env |

## 🚀 Extensões Futuras

### Funcionalidades Sugeridas
1. **Autenticação e Autorização**
   - JWT tokens
   - Refresh tokens
   - Permissões por role

2. **Pagamentos**
   - Integração com Stripe/PagSeguro
   - Histórico de transações

3. **Notificações**
   - Email (confirmação de agendamento)
   - SMS (lembrete de aula)
   - Push notifications

4. **Avaliações**
   - Sistema de rating para instrutores
   - Comentários de alunos

5. **Uploads**
   - Foto de perfil
   - Documentos (CNH, credencial)

6. **Relatórios**
   - Dashboard de estatísticas
   - Relatórios financeiros

7. **Validações Avançadas**
   - Verificar conflitos de horário
   - Validar disponibilidade real
   - Calcular distância entre aluno e instrutor

### Estrutura Sugerida para Expansão
```
app/
├── services/          # Lógica de negócio complexa
├── utils/             # Funções auxiliares
├── middleware/        # Middlewares customizados
├── exceptions/        # Exceções customizadas
└── dependencies/      # Dependencies reutilizáveis
```

## 📝 Convenções de Código

### Nomenclatura
- **Arquivos**: snake_case (`instructor_profile.py`)
- **Classes**: PascalCase (`InstructorProfile`)
- **Funções**: snake_case (`create_user`)
- **Constantes**: UPPER_CASE (`BASE_URL`)

### Docstrings
Todas as funções públicas têm docstrings descritivas.

### Type Hints
Todo o código usa type hints do Python para melhor IDE support.

---

**Esta estrutura foi projetada para ser:**
- ✅ Escalável
- ✅ Manutenível
- ✅ Testável
- ✅ Fácil de entender
