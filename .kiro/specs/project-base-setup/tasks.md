# Plano de Implementação: Estrutura Base do Projeto

## Visão Geral

Configurar a estrutura base do monorepo Dashboard de Produtividade Dev com dois subprojetos Python independentes (backend FastAPI + frontend Streamlit), gerenciados via `uv`, com variáveis de ambiente documentadas, convenções de código via Ruff, e aplicações mínimas funcionais.

## Tarefas

- [x] 1. Configurar subprojeto Backend com `uv` e dependências
  - [x] 1.1 Inicializar o projeto backend com `uv init` e criar `pyproject.toml`
    - Criar `backend/pyproject.toml` com nome `dashboard-produtividade-backend`, versão `0.1.0`, `requires-python = ">=3.12"`
    - Declarar dependências de produção: fastapi, uvicorn, loguru, python-dotenv, langchain, chromadb, aisuite, sqlite-utils
    - Declarar dependências de desenvolvimento via `[dependency-groups]`: pytest, ruff
    - Configurar seção `[tool.ruff]` com `target-version = "py312"`, `line-length = 88`, `select = ["E", "F", "W", "I"]`
    - Criar arquivo `backend/.python-version` com conteúdo `3.12`
    - _Requisitos: 2.1, 2.2, 2.3, 2.5, 9.1_

  - [x] 1.2 Criar estrutura de pacotes do backend
    - Criar arquivo `backend/src/__init__.py` (vazio) para marcar `src` como pacote Python
    - Garantir existência de `backend/tests/` e `backend/docs/`
    - _Requisitos: 1.1, 1.2_

- [x] 2. Configurar subprojeto Frontend com `uv` e dependências
  - [x] 2.1 Inicializar o projeto frontend com `uv init` e criar `pyproject.toml`
    - Criar `frontend/pyproject.toml` com nome `dashboard-produtividade-frontend`, versão `0.1.0`, `requires-python = ">=3.12"`
    - Declarar dependências de produção: streamlit, plotly, python-dotenv, requests
    - Declarar dependências de desenvolvimento via `[dependency-groups]`: pytest, ruff
    - Configurar seção `[tool.ruff]` com `target-version = "py312"`, `line-length = 88`, `select = ["E", "F", "W", "I"]`
    - Criar arquivo `frontend/.python-version` com conteúdo `3.12`
    - _Requisitos: 3.1, 3.2, 3.3, 3.5, 9.2_

  - [x] 2.2 Criar estrutura de pacotes do frontend
    - Criar arquivo `frontend/src/__init__.py` (vazio) para marcar `src` como pacote Python
    - Garantir existência de `frontend/tests/` e `frontend/docs/`
    - _Requisitos: 1.1, 1.3_

- [x] 3. Configurar variáveis de ambiente e proteção de dados sensíveis
  - [x] 3.1 Criar arquivos `.env.example` com variáveis e placeholders
    - Atualizar `backend/.env.example` com todas as variáveis obrigatórias: GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_GRAPHQL_URL, CHROMADB_PATH, SQLITE_DB_PATH, LOG_LEVEL, OLLAMA_BASE_URL, OLLAMA_MODEL, EMBEDDING_MODEL, APP_PORT
    - Cada variável deve ter um valor placeholder descritivo (ex: `GITHUB_TOKEN=seu_token_aqui`)
    - Atualizar `frontend/.env.example` com: BACKEND_API_URL=http://localhost:8000, STREAMLIT_SERVER_PORT=8501
    - _Requisitos: 4.1, 4.2, 4.3, 4.4_

  - [x] 3.2 Atualizar `.gitignore` com regras de segurança
    - Adicionar regras para excluir: `.env`, `.venv/`, `__pycache__/`, `*.db`, `*.sqlite`, `*.sqlite3`, `chroma_data/`
    - _Requisitos: 5.1, 5.2, 5.3, 5.4_

- [x] 4. Checkpoint — Verificar configuração dos subprojetos
  - Garantir que `uv sync` executa sem erros em `backend/` e `frontend/`
  - Garantir que `uv run ruff check .` passa sem violações em ambos subprojetos
  - Perguntar ao usuário se há dúvidas antes de prosseguir

- [x] 5. Implementar aplicação mínima do Backend (FastAPI)
  - [x] 5.1 Criar `backend/src/main.py` com aplicação FastAPI mínima
    - Configurar Loguru como sistema de logging padrão no startup da aplicação
    - Carregar variáveis de ambiente via `python-dotenv` (falha silenciosa se `.env` não existir)
    - Usar `LOG_LEVEL` do `.env` com fallback para `DEBUG`
    - Implementar rota `GET /health` retornando `{"status": "healthy"}` com status HTTP 200
    - _Requisitos: 7.1, 7.2, 7.3, 7.4_

  - [x] 5.2 Escrever testes unitários para a rota `/health`
    - Usar `TestClient` do FastAPI para verificar status 200 e JSON `{"status": "healthy"}`
    - Criar arquivo `backend/tests/test_main.py`
    - _Requisitos: 7.3_

- [x] 6. Implementar aplicação mínima do Frontend (Streamlit)
  - [x] 6.1 Criar `frontend/src/app.py` com aplicação Streamlit mínima
    - Carregar variáveis de ambiente via `python-dotenv` (falha silenciosa se `.env` não existir)
    - Renderizar título `st.title("Dashboard de Produtividade Dev")`
    - _Requisitos: 8.1, 8.2, 8.3_

  - [x] 6.2 Escrever teste unitário para verificar conteúdo do `app.py`
    - Verificar que `app.py` contém a chamada `st.title("Dashboard de Produtividade Dev")`
    - Criar arquivo `frontend/tests/test_app.py`
    - _Requisitos: 8.3_

- [x] 7. Checkpoint — Verificar aplicações mínimas
  - Garantir que todos os testes passam em ambos subprojetos
  - Garantir que `uv run ruff check .` continua sem violações
  - Perguntar ao usuário se há dúvidas antes de prosseguir

- [x] 8. Atualizar README.md com instruções de setup
  - [x] 8.1 Reescrever `README.md` na raiz do repositório
    - Incluir descrição do projeto Dashboard de Produtividade Dev
    - Listar pré-requisitos: Python 3.12, uv, Ollama
    - Instruções passo a passo para setup do Backend: clonar repo, copiar `.env.example` para `.env`, executar `uv sync`, executar `uv run uvicorn src.main:app --reload`
    - Instruções passo a passo para setup do Frontend: copiar `.env.example` para `.env`, executar `uv sync`, executar `uv run streamlit run src/app.py`
    - Incluir estrutura de diretórios do projeto
    - Listar stack técnica: FastAPI, Streamlit, Plotly, ChromaDB, Ollama, loguru, aisuite, SQLite
    - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [x] 9. Testes de propriedade e validação final
  - [x] 9.1 Escrever teste de propriedade para presença de variáveis obrigatórias nos `.env.example`
    - **Propriedade 1: Presença de variáveis obrigatórias nos arquivos .env.example**
    - Usar `hypothesis` para gerar subprojeto aleatório (backend/frontend) e variável aleatória da lista obrigatória
    - Verificar que a variável está presente no `.env.example` correspondente
    - Mínimo 100 iterações
    - **Valida: Requisitos 4.1, 4.2**

  - [x] 9.2 Escrever teste de propriedade para placeholders não-vazios nos `.env.example`
    - **Propriedade 2: Placeholders não-vazios nos arquivos .env.example**
    - Usar `hypothesis` para gerar pares aleatórios (arquivo, variável) e verificar que o valor após `=` não é vazio
    - Mínimo 100 iterações
    - **Valida: Requisitos 4.3, 4.4**

  - [x] 9.3 Escrever testes unitários de validação estrutural
    - Verificar existência de todos os diretórios obrigatórios (Req 1.1)
    - Verificar existência de `__init__.py` em `backend/src/` e `frontend/src/` (Req 1.2, 1.3)
    - Verificar conteúdo de `.python-version` em ambos subprojetos (Req 2.5, 3.5)
    - Verificar presença de padrões no `.gitignore` (Req 5.1–5.4)
    - Verificar seção `[tool.ruff]` nos `pyproject.toml` de ambos subprojetos (Req 9.1, 9.2)
    - _Requisitos: 1.1, 1.2, 1.3, 2.5, 3.5, 5.1–5.4, 9.1, 9.2_

- [x] 10. Checkpoint final — Garantir que todos os testes passam
  - Executar todos os testes em ambos subprojetos
  - Garantir que `uv run ruff check .` passa sem violações em ambos
  - Perguntar ao usuário se há dúvidas

## Notas

- Tarefas marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada tarefa referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Testes de propriedade validam propriedades universais de corretude
- Testes unitários validam exemplos concretos e casos específicos
- Todo gerenciamento de dependências DEVE usar `uv` (nunca pip, poetry ou requirements.txt)
