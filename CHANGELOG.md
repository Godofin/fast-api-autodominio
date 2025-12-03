# 📝 Changelog - AutoDomínio API

## [2.0.0] - 03/12/2024

### ✨ Novas Funcionalidades

#### Sistema de Avaliações (Reviews)
- ✅ Adicionada tabela `reviews` no banco de dados
- ✅ Endpoint para criar avaliações (POST `/reviews/`)
- ✅ Endpoint para listar avaliações de instrutor (GET `/reviews/instructor/{id}`)
- ✅ Endpoint para estatísticas de avaliação (GET `/reviews/instructor/{id}/stats`)
- ✅ Validação: apenas agendamentos concluídos podem ser avaliados
- ✅ Validação: cada agendamento pode ter apenas uma avaliação
- ✅ Rating de 1 a 5 estrelas com comentário opcional

#### Sistema de Aprovação de Instrutores
- ✅ Adicionados campos em `instructor_profiles`:
  - `approval_status` (pending/approved/rejected/under_review)
  - `approval_date`
  - `rejection_reason`
- ✅ Endpoint para listar instrutores pendentes (GET `/instructor-approval/pending`)
- ✅ Endpoint para listar instrutores em análise (GET `/instructor-approval/under-review`)
- ✅ Endpoint para listar instrutores aprovados (GET `/instructor-approval/approved`)
- ✅ Endpoint para listar instrutores rejeitados (GET `/instructor-approval/rejected`)
- ✅ Endpoint para atualizar status (PATCH `/instructor-approval/{id}/status`)
- ✅ Endpoint para estatísticas de aprovação (GET `/instructor-approval/stats`)
- ✅ Instrutores criados com status `pending` por padrão

#### Upload de Fotos de Perfil
- ✅ Adicionado campo `profile_photo` na tabela `users`
- ✅ Endpoint para upload de foto (POST `/uploads/profile-photo/{user_id}`)
- ✅ Suporte para formatos: .jpg, .jpeg, .png, .gif, .webp
- ✅ Foto antiga é deletada automaticamente ao fazer novo upload
- ✅ Arquivos salvos em `uploads/profile_photos/`

#### Upload de Documentos de Instrutores
- ✅ Adicionada tabela `instructor_documents` no banco de dados
- ✅ Endpoint para upload de documentos (POST `/uploads/instructor-document/{id}`)
- ✅ Endpoint para listar documentos (GET `/uploads/instructor-documents/{id}`)
- ✅ Endpoint para deletar documentos (DELETE `/uploads/instructor-document/{id}`)
- ✅ Suporte para formatos: .pdf, .jpg, .jpeg, .png, .doc, .docx
- ✅ Tipos de documentos suportados:
  - CNH (Carteira Nacional de Habilitação)
  - Credencial de Instrutor
  - Certificado do curso
  - RG, CPF
  - Comprovante de residência
  - Documento do veículo
  - Outros
- ✅ Arquivos salvos em `uploads/documents/`

#### Endpoint de Informações
- ✅ GET `/uploads/info` - Informações sobre uploads permitidos

### 🔧 Melhorias

#### Schemas Atualizados
- ✅ `UserBase` e `UserUpdate` incluem campo `profile_photo`
- ✅ `InstructorProfileResponse` inclui campos de aprovação
- ✅ Novos schemas: `ReviewCreate`, `ReviewUpdate`, `ReviewResponse`
- ✅ Novos schemas: `InstructorDocumentCreate`, `InstructorDocumentResponse`
- ✅ Novo schema: `InstructorApprovalUpdate`
- ✅ Novo schema: `InstructorRatingStats`

#### Modelos Atualizados
- ✅ Modelo `User` com campo `profile_photo`
- ✅ Modelo `InstructorProfile` com campos de aprovação
- ✅ Novos modelos: `Review`, `InstructorDocument`
- ✅ Novos enums: `ApprovalStatus`, `DocumentType`

### 📦 Dependências

#### Adicionadas
- ✅ `python-multipart==0.0.6` - Para upload de arquivos

### 📊 Estatísticas

- **Novos Endpoints:** 18
- **Total de Endpoints:** 45
- **Novas Tabelas:** 2
- **Total de Tabelas:** 7
- **Novos Arquivos de Código:** 8

### 📁 Novos Arquivos

#### Models
- `app/models/review.py`
- `app/models/instructor_document.py`

#### Schemas
- `app/schemas/review.py`
- `app/schemas/instructor_document.py`
- `app/schemas/instructor_approval.py`

#### Routes
- `app/routes/reviews.py`
- `app/routes/instructor_approval.py`
- `app/routes/uploads.py`

#### Documentação
- `NOVAS_FUNCIONALIDADES.md`
- `CHANGELOG.md` (este arquivo)

---

## [1.0.1] - 03/12/2024

### 🐛 Correções de Bugs

- ✅ Removido constraint inválido `decimal_places` dos schemas
- ✅ Adicionada dependência `email-validator==2.1.0`

---

## [1.0.0] - 03/12/2024

### ✨ Lançamento Inicial

#### Funcionalidades Básicas
- ✅ Gestão de usuários (alunos, instrutores, admins)
- ✅ Perfis de instrutores com informações detalhadas
- ✅ Sistema de disponibilidade semanal
- ✅ Sistema de agendamentos de aulas
- ✅ Exceções de agenda (dias bloqueados)
- ✅ Busca de instrutores com filtros

#### Tecnologias
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- Uvicorn 0.24.0
- SQLite (desenvolvimento)

#### Endpoints Iniciais
- 5 módulos de rotas
- 27 endpoints REST
- Documentação automática (Swagger/ReDoc)

---

## 🔮 Próximas Versões (Planejado)

### [2.1.0] - Futuro
- [ ] Autenticação JWT
- [ ] Permissões por role
- [ ] Refresh tokens

### [2.2.0] - Futuro
- [ ] Integração com sistema de pagamentos
- [ ] Histórico de transações
- [ ] Relatórios financeiros

### [2.3.0] - Futuro
- [ ] Sistema de notificações (email/SMS)
- [ ] Lembretes de aula
- [ ] Confirmações automáticas

### [3.0.0] - Futuro
- [ ] Validação automática de conflitos de horário
- [ ] Cálculo de distância entre aluno e instrutor
- [ ] Sistema de recomendação de instrutores
- [ ] Dashboard administrativo
- [ ] Relatórios e analytics

---

## 📝 Notas de Migração

### De 1.x para 2.0

#### Banco de Dados
O banco de dados será atualizado automaticamente na primeira execução. As seguintes mudanças serão aplicadas:

1. **Novas tabelas criadas:**
   - `reviews`
   - `instructor_documents`

2. **Colunas adicionadas:**
   - `users.profile_photo`
   - `instructor_profiles.approval_status`
   - `instructor_profiles.approval_date`
   - `instructor_profiles.rejection_reason`

3. **Dados existentes:**
   - ✅ Todos os dados existentes são preservados
   - ✅ Instrutores existentes recebem status `pending` automaticamente
   - ✅ Compatibilidade total com versão anterior

#### Código
- ✅ Todos os endpoints anteriores continuam funcionando
- ✅ Nenhuma breaking change
- ✅ Apenas adições de funcionalidades

#### Instalação
```bash
# Atualizar dependências
pip install -r requirements.txt

# Executar API (atualização automática do banco)
python main.py
```

---

## 🤝 Contribuições

Este projeto está em desenvolvimento ativo. Sugestões e melhorias são bem-vindas!

---

**Mantido por:** Equipe AutoDomínio
**Licença:** MIT (sugerido)
