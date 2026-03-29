---
inclusion: fileMatch
fileMatchPattern: "backend/**"
---

# Diretrizes — Backend

## Stack

- Framework: FastAPI + Uvicorn
- ORM: SQLModel (SQLAlchemy + Pydantic unificados)
- Banco relacional: SQLite via SQLModel
- Banco vetorial: ChromaDB (modo embedded, sem servidor)
- RAG: pipeline customizado com aisuite (provider-agnostic para LLM)
- Embeddings: `all-MiniLM-L6-v2` via sentence-transformers (384D)
- LLM: Ollama (`llama3.1`) local ou OpenAI (`gpt-4o-mini`) via aisuite
- Rate limiting: slowapi
- Logging: loguru com correlation IDs
- Scheduler: APScheduler (ingestão a cada 12h)

## Estrutura de Pastas

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py             # App FastAPI, CORS, rate limiting, scheduler
│   ├── config.py           # Pydantic Settings (.env)
│   ├── database.py         # Engine SQLModel, get_session
│   ├── logging_config.py   # Loguru + correlation IDs
│   ├── github/             # Coleta via GraphQL
│   ├── rag/                # Embeddings, vector store, LLM, pipeline
│   ├── routes/             # Endpoints REST
│   └── services/           # Ingestão + métricas
├── tests/
├── pyproject.toml
└── .python-version         # 3.12
```

## Gerenciamento de Dependências

- SEMPRE usar `uv add` para adicionar dependências de produção
- SEMPRE usar `uv add --dev` para dependências de desenvolvimento
- SEMPRE usar `uv run` para executar código
- SEMPRE commitar `uv.lock`
- NUNCA usar `pip`, `poetry` ou `requirements.txt`

## Execução

```bash
cd backend
cp .env.example .env
# Editar .env com GITHUB_TOKEN e GITHUB_USERNAME
uv sync
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Variáveis de Ambiente (`backend/.env`)

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=seu_usuario

LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
OPENAI_API_KEY=

CHROMA_PATH=./data/chroma
CHROMA_COLLECTION=github_activity

SQLITE_DB_PATH=./data.db

INGESTION_DAYS_BACK=90

CORS_ORIGINS=["http://localhost:8501"]
```

## Testes

- Testes unitários com pytest para toda funcionalidade nova
- Testes de propriedade com hypothesis quando aplicável
- Executar: `uv run pytest`
