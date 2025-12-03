# 🪟 Guia Rápido - Windows

Este guia mostra passo a passo como executar a API AutoDomínio no Windows.

## ✅ Pré-requisitos

1. **Python 3.11 ou superior** instalado
   - Baixe em: https://www.python.org/downloads/
   - Durante a instalação, marque a opção "Add Python to PATH"

2. **Verificar instalação do Python**
   - Abra o **Prompt de Comando** (cmd) ou **PowerShell**
   - Digite: `python --version`
   - Deve aparecer algo como: `Python 3.11.x`

## 🚀 Passo a Passo

### 1. Navegar até a pasta do projeto

Abra o **Prompt de Comando** ou **PowerShell** e navegue até a pasta onde está o projeto:

```bash
cd C:\caminho\para\autodominio
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

**Aguarde a instalação**. Você verá mensagens como:
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

### 3. Executar a API

```bash
python main.py
```

**Você verá algo assim:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **A API está rodando!**

### 4. Testar a API

**Opção 1: Navegador**
- Abra seu navegador
- Acesse: http://localhost:8000/docs
- Você verá a documentação interativa (Swagger UI)

**Opção 2: Script de teste**
- Abra **outro** Prompt de Comando (mantenha o primeiro rodando a API)
- Navegue até a pasta do projeto
- Execute:
```bash
python test_api.py
```

Este script irá criar dados de exemplo e testar todos os endpoints!

### 5. Parar a API

Para parar o servidor, pressione `CTRL + C` no terminal onde a API está rodando.

## 📝 Comandos Úteis

### Limpar o banco de dados

Se quiser recomeçar do zero, delete o arquivo do banco:

```bash
del autodominio.db
```

Depois execute a API novamente com `python main.py`

### Verificar se a API está rodando

Acesse no navegador: http://localhost:8000/health

Deve retornar:
```json
{"status": "healthy"}
```

## 🔧 Solução de Problemas

### Erro: "python não é reconhecido como comando"

**Solução:** Python não está no PATH do Windows
1. Desinstale e reinstale o Python
2. Marque a opção "Add Python to PATH" durante a instalação

### Erro: "No module named 'fastapi'"

**Solução:** Dependências não foram instaladas
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use" ou porta 8000 ocupada

**Solução:** Outra aplicação está usando a porta 8000

Opção 1 - Encontrar e fechar o processo:
```bash
netstat -ano | findstr :8000
taskkill /PID [número_do_processo] /F
```

Opção 2 - Usar outra porta:
Edite o arquivo `main.py` e mude a linha:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```
Para:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
```

### Erro ao instalar dependências

**Solução:** Atualizar o pip
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 🎯 Testando Manualmente com cURL (Windows)

Se você tem o Git Bash ou WSL instalado, pode usar cURL:

### Criar um usuário:
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"João Silva\",\"email\":\"joao@email.com\",\"password\":\"senha123\",\"role\":\"student\",\"phone\":\"11999999999\"}"
```

### Listar usuários:
```bash
curl http://localhost:8000/users/
```

## 📱 Testando com Postman ou Insomnia

1. Baixe o **Postman** (https://www.postman.com/) ou **Insomnia** (https://insomnia.rest/)
2. Importe a coleção da API acessando: http://localhost:8000/openapi.json
3. Teste os endpoints visualmente

## 🌐 Acessar de outro dispositivo na mesma rede

1. Descubra seu IP local:
```bash
ipconfig
```
Procure por "Endereço IPv4" (ex: 192.168.1.100)

2. No outro dispositivo, acesse:
```
http://192.168.1.100:8000
```

**Nota:** Pode ser necessário liberar a porta 8000 no Firewall do Windows.

## 📚 Próximos Passos

Depois de testar localmente:
1. Leia o arquivo `README.md` para entender a estrutura completa
2. Explore os endpoints em http://localhost:8000/docs
3. Modifique o código conforme suas necessidades
4. Considere adicionar autenticação JWT para produção

---

**Dúvidas?** Consulte o arquivo `README.md` para documentação completa! 🚀
