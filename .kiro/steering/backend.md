---
inclusion: fileMatch
fileMatchPattern: "backend/**"
---

# Diretrizes — Backend

## Stack

- Framework: FastAPI + Uvicorn
- ORM: SQLModel (SQLAlchemy + Pydantic unificados)
- Banco relacional: SQLite via `sqlite-utils` e SQLModel
- Banco vetorial: ChromaDB (modo embedded, sem servidor)
- RAG: LangChain + aisuite (provider-agnostic para LLM)
- Embeddings: `intfloat/multilingual-e5-large` via HuggingFace
- LLM: Ollama (Llama 3.1 8B) local
- Logging: Loguru (configurado via LOG_LEVEL do .env)
- Variáveis de ambiente: python-dotenv
- Porta configurável via APP_PORT no .env (default 8000)

## Estrutura de Pastas

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # App FastAPI, startup, health check
│   ├── database.py       # Engine SQLModel, get_session
│   └── models/           # Entidades SQLModel (table=True)
│       └── __init__.py   # Exporta todos os modelos
├── tests/
├── docs/
├── pyproject.toml
└── .python-version       # 3.12
```

## Banco de Dados — SQLModel

- Criar modelos em `backend/src/models/` (um arquivo por domínio)
- Exportar no `backend/src/models/__init__.py`
- Importar no `main.py` para registrar no metadata
- Sempre criar schemas separados: `ModelCreate` (request) e `ModelRead` (response) sem `table=True`
- Usar `Field(primary_key=True)` com `default=None` para autoincrement
- Usar `Field(index=True)` em campos usados em buscas frequentes
- Tabelas criadas automaticamente no startup via `create_db_and_tables()`

## ChromaDB

- Modo embedded (biblioteca Python, sem servidor Docker)
- Dados salvos em `CHROMADB_PATH` (default `./chroma_data`)
- Usado para armazenar embeddings de commits, PRs e issues

## Gerenciamento de Dependências

- SEMPRE usar `uv add` para adicionar dependências
- SEMPRE usar `uv add --dev` para dependências de desenvolvimento
- SEMPRE usar `uv run` para executar código
- SEMPRE commitar `uv.lock`
- NUNCA usar `pip`, `poetry` ou `requirements.txt`

## Execução

```bash
cd backend
cp .env.example .env
uv sync
uv run python -m src.main
```

## Variáveis de Ambiente (`backend/.env`)

```env
GITHUB_TOKEN=seu_token_aqui
GITHUB_USERNAME=seu_usuario_aqui
GITHUB_GRAPHQL_URL=https://api.github.com/graphql
CHROMADB_PATH=./chroma_data
SQLITE_DB_PATH=./data.db
LOG_LEVEL=DEBUG
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
EMBEDDING_MODEL=intfloat/multilingual-e5-large
APP_PORT=8000
```

## Testes

- Testes unitários com pytest para toda funcionalidade nova
- Testes de propriedade com hypothesis quando aplicável
- Executar: `uv run pytest`
