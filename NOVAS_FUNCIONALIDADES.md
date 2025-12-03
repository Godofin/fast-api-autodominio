# 🎉 Novas Funcionalidades - Versão 2.0

## 📋 Resumo das Adições

A API AutoDomínio foi expandida com **3 novos módulos** e **8 novas tabelas/funcionalidades**:

1. ⭐ **Sistema de Avaliações (Reviews)**
2. ✅ **Sistema de Aprovação de Instrutores**
3. 📸 **Upload de Fotos de Perfil**
4. 📄 **Upload de Documentos de Instrutores**

---

## ⭐ 1. Sistema de Avaliações (Reviews)

### Nova Tabela: `reviews`

Permite que alunos avaliem instrutores após aulas concluídas.

**Campos:**
- `id` - Identificador único
- `appointment_id` - ID do agendamento (único)
- `student_id` - ID do aluno que avaliou
- `instructor_id` - ID do instrutor avaliado
- `rating` - Nota de 1 a 5 estrelas
- `comment` - Comentário opcional
- `created_at` - Data da avaliação

### Novos Endpoints: `/reviews`

#### POST `/reviews/`
Criar uma nova avaliação (apenas para agendamentos concluídos).

**Request Body:**
```json
{
  "appointment_id": 1,
  "instructor_id": 2,
  "rating": 5,
  "comment": "Excelente instrutor! Muito paciente e didático."
}
```

#### GET `/reviews/instructor/{instructor_id}`
Listar todas as avaliações de um instrutor.

**Response:**
```json
[
  {
    "id": 1,
    "appointment_id": 1,
    "student_id": 1,
    "instructor_id": 2,
    "rating": 5,
    "comment": "Excelente instrutor!",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### GET `/reviews/instructor/{instructor_id}/stats`
Obter estatísticas de avaliação do instrutor.

**Response:**
```json
{
  "instructor_id": 2,
  "average_rating": 4.75,
  "total_reviews": 12,
  "rating_distribution": {
    "1": 0,
    "2": 0,
    "3": 1,
    "4": 3,
    "5": 8
  }
}
```

#### PUT `/reviews/{review_id}`
Atualizar uma avaliação existente.

#### DELETE `/reviews/{review_id}`
Deletar uma avaliação.

---

## ✅ 2. Sistema de Aprovação de Instrutores

### Campos Adicionados em `instructor_profiles`

- `approval_status` - Status da aprovação (pending/approved/rejected/under_review)
- `approval_date` - Data da aprovação/rejeição
- `rejection_reason` - Motivo da rejeição (se aplicável)

### Status Possíveis:

| Status | Descrição |
|--------|-----------|
| `pending` | Aguardando aprovação (padrão) |
| `under_review` | Em análise pela equipe |
| `approved` | Aprovado - pode dar aulas |
| `rejected` | Rejeitado - não pode dar aulas |

### Novos Endpoints: `/instructor-approval`

#### GET `/instructor-approval/pending`
Listar instrutores aguardando aprovação.

#### GET `/instructor-approval/under-review`
Listar instrutores em análise.

#### GET `/instructor-approval/approved`
Listar instrutores aprovados.

#### GET `/instructor-approval/rejected`
Listar instrutores rejeitados.

#### PATCH `/instructor-approval/{instructor_profile_id}/status`
Atualizar status de aprovação de um instrutor.

**Request Body:**
```json
{
  "approval_status": "approved",
  "rejection_reason": null
}
```

Ou para rejeitar:
```json
{
  "approval_status": "rejected",
  "rejection_reason": "Documentação incompleta"
}
```

#### PATCH `/instructor-approval/{instructor_profile_id}/set-under-review`
Marcar instrutor como "em análise".

#### GET `/instructor-approval/stats`
Obter estatísticas de aprovação.

**Response:**
```json
{
  "approval_stats": {
    "pending": 5,
    "under_review": 3,
    "approved": 25,
    "rejected": 2
  },
  "total_instructors": 35
}
```

---

## 📸 3. Upload de Fotos de Perfil

### Campo Adicionado em `users`

- `profile_photo` - Caminho da foto de perfil (opcional)

### Novos Endpoints: `/uploads`

#### POST `/uploads/profile-photo/{user_id}`
Upload de foto de perfil do usuário.

**Como usar:**
- Método: POST
- Content-Type: multipart/form-data
- Campo: `file` (arquivo de imagem)

**Extensões permitidas:** .jpg, .jpeg, .png, .gif, .webp

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/uploads/profile-photo/1" \
  -F "file=@minha_foto.jpg"
```

**Response:**
```json
{
  "message": "Foto de perfil enviada com sucesso",
  "user_id": 1,
  "file_path": "uploads/profile_photos/abc123.jpg"
}
```

---

## 📄 4. Upload de Documentos de Instrutores

### Nova Tabela: `instructor_documents`

Armazena documentos enviados pelos instrutores para validação.

**Campos:**
- `id` - Identificador único
- `instructor_id` - ID do perfil do instrutor
- `document_type` - Tipo do documento
- `file_path` - Caminho do arquivo
- `original_filename` - Nome original do arquivo
- `uploaded_at` - Data do upload

### Tipos de Documentos Aceitos:

| Tipo | Descrição |
|------|-----------|
| `cnh` | Carteira Nacional de Habilitação |
| `credential` | Credencial de Instrutor |
| `certificate` | Certificado do curso de instrutor |
| `rg` | Registro Geral |
| `cpf` | Cadastro de Pessoa Física |
| `proof_of_address` | Comprovante de residência |
| `vehicle_document` | Documento do veículo |
| `other` | Outros documentos |

### Endpoints de Documentos

#### POST `/uploads/instructor-document/{instructor_profile_id}`
Upload de documento do instrutor.

**Como usar:**
- Método: POST
- Content-Type: multipart/form-data
- Campos:
  - `file` (arquivo)
  - `document_type` (tipo do documento)

**Extensões permitidas:** .pdf, .jpg, .jpeg, .png, .doc, .docx

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/uploads/instructor-document/1" \
  -F "file=@cnh.pdf" \
  -F "document_type=cnh"
```

**Response:**
```json
{
  "id": 1,
  "instructor_id": 1,
  "document_type": "cnh",
  "file_path": "uploads/documents/xyz789.pdf",
  "original_filename": "cnh.pdf",
  "uploaded_at": "2024-01-15T10:30:00"
}
```

#### GET `/uploads/instructor-documents/{instructor_profile_id}`
Listar todos os documentos de um instrutor.

#### DELETE `/uploads/instructor-document/{document_id}`
Deletar um documento.

#### GET `/uploads/info`
Obter informações sobre uploads permitidos.

---

## 🔄 Fluxo de Aprovação de Instrutor

### Passo a Passo:

1. **Instrutor se cadastra**
   - Cria usuário com role "instructor"
   - Cria perfil de instrutor
   - Status inicial: `pending`

2. **Instrutor envia documentos**
   - Upload de CNH
   - Upload de credencial de instrutor
   - Upload de certificado
   - Upload de outros documentos necessários

3. **Admin analisa**
   - Marca como `under_review`
   - Verifica documentos
   - Verifica informações

4. **Admin decide**
   - **Aprovar:** Status → `approved`
   - **Rejeitar:** Status → `rejected` + motivo

5. **Instrutor aprovado pode:**
   - Definir disponibilidade
   - Receber agendamentos
   - Dar aulas

---

## 📊 Estatísticas Disponíveis

### Avaliações de Instrutor
- Média de rating
- Total de avaliações
- Distribuição de notas (1-5 estrelas)

### Aprovação de Instrutores
- Total por status
- Total geral de instrutores

---

## 🎯 Exemplo de Uso Completo

### 1. Criar Instrutor
```bash
POST /users/
{
  "name": "Carlos Instrutor",
  "email": "carlos@email.com",
  "password": "senha123",
  "role": "instructor",
  "phone": "11999999999"
}
```

### 2. Criar Perfil do Instrutor
```bash
POST /instructor-profiles/
{
  "user_id": 2,
  "bio": "Instrutor experiente",
  "credential_number": "DETRAN-SP-12345",
  "hourly_rate": 80.00,
  "car_model": "Gol",
  "transmission": "manual",
  "city": "São Paulo"
}
```
**Status inicial:** `pending`

### 3. Upload de Foto de Perfil
```bash
POST /uploads/profile-photo/2
Form-data: file=foto.jpg
```

### 4. Upload de Documentos
```bash
POST /uploads/instructor-document/1
Form-data: 
  - file=cnh.pdf
  - document_type=cnh

POST /uploads/instructor-document/1
Form-data:
  - file=credencial.pdf
  - document_type=credential
```

### 5. Admin Aprova
```bash
PATCH /instructor-approval/1/status
{
  "approval_status": "approved",
  "rejection_reason": null
}
```

### 6. Instrutor Define Disponibilidade
```bash
POST /instructor-availability/
{
  "instructor_id": 1,
  "day_of_week": 1,
  "start_time": "08:00:00",
  "end_time": "18:00:00",
  "is_active": true
}
```

### 7. Aluno Agenda Aula
```bash
POST /appointments/
{
  "student_id": 1,
  "instructor_id": 2,
  "start_date": "2024-01-20T14:00:00",
  "end_date": "2024-01-20T15:00:00",
  "location_pickup": "Av. Paulista, 1000",
  "notes": "Preciso praticar baliza"
}
```

### 8. Aula Concluída - Aluno Avalia
```bash
PATCH /appointments/1/status?new_status=completed

POST /reviews/
{
  "appointment_id": 1,
  "instructor_id": 2,
  "rating": 5,
  "comment": "Excelente instrutor!"
}
```

### 9. Ver Estatísticas do Instrutor
```bash
GET /reviews/instructor/2/stats
```

---

## 📁 Estrutura de Arquivos

```
uploads/
├── profile_photos/     # Fotos de perfil
│   ├── abc123.jpg
│   └── def456.png
└── documents/          # Documentos dos instrutores
    ├── xyz789.pdf
    └── qwe321.jpg
```

**Nota:** A pasta `uploads/` é criada automaticamente na primeira execução.

---

## 🔒 Segurança

### Validações Implementadas:

✅ Apenas agendamentos concluídos podem ser avaliados
✅ Cada agendamento pode ter apenas uma avaliação
✅ Rating deve estar entre 1 e 5
✅ Extensões de arquivo validadas
✅ Motivo obrigatório ao rejeitar instrutor
✅ Arquivos antigos são deletados ao fazer novo upload

---

## 🆕 Novos Endpoints - Resumo

| Módulo | Endpoints | Total |
|--------|-----------|-------|
| Reviews | 6 | 6 |
| Instructor Approval | 7 | 7 |
| Uploads | 5 | 5 |
| **TOTAL NOVOS** | | **18** |
| **TOTAL GERAL** | | **45** |

---

## 📝 Atualizações no Banco de Dados

### Novas Tabelas:
1. `reviews` - Avaliações
2. `instructor_documents` - Documentos dos instrutores

### Tabelas Atualizadas:
1. `users` - Adicionado campo `profile_photo`
2. `instructor_profiles` - Adicionados campos:
   - `approval_status`
   - `approval_date`
   - `rejection_reason`

---

## 🚀 Como Testar

### 1. Instalar dependências atualizadas:
```bash
pip install -r requirements.txt
```

### 2. Executar a API:
```bash
python main.py
```

### 3. Acessar documentação:
http://localhost:8000/docs

### 4. Testar uploads:
Use a interface Swagger UI em `/docs` para testar uploads de forma visual!

---

## 💡 Dicas de Uso

### Para Admins:
- Use `/instructor-approval/pending` para ver quem precisa ser aprovado
- Use `/instructor-approval/stats` para monitorar o processo
- Sempre forneça um motivo ao rejeitar um instrutor

### Para Instrutores:
- Envie todos os documentos necessários antes de solicitar aprovação
- Mantenha sua foto de perfil atualizada
- Monitore suas avaliações em `/reviews/instructor/{seu_id}/stats`

### Para Alunos:
- Avalie os instrutores após as aulas para ajudar outros alunos
- Veja as estatísticas dos instrutores antes de agendar

---

**Versão:** 2.0
**Data:** 03/12/2024
**Compatibilidade:** Totalmente compatível com versão 1.x
