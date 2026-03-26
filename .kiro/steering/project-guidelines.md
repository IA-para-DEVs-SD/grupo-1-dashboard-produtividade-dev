# Diretrizes do Projeto — Dashboard de Produtividade Dev

## Visão Geral

Dashboard full-stack local-first que coleta dados do GitHub, processa com embeddings e responde perguntas via RAG. Todo processamento é local, sem serviços externos pagos.

## Arquitetura

- Monorepo com dois subprojetos Python independentes: `backend/` e `frontend/`
- Cada subprojeto tem seu próprio `pyproject.toml`, `.venv/` e `uv.lock`
- Gerenciamento exclusivo via `uv` — NUNCA usar pip, poetry ou requirements.txt

### Backend (`backend/`)

- Framework: FastAPI + Uvicorn
- ORM: SQLModel (SQLAlchemy + Pydantic unificados)
- Banco relacional: SQLite via `sqlite-utils` e SQLModel
- Banco vetorial: ChromaDB (modo embedded, sem servidor)
- RAG: LangChain + aisuite (provider-agnostic para LLM)
- Embeddings: `intfloat/multilingual-e5-large` via HuggingFace
- LLM: Ollama (Llama 3.1 8B) local
- Logging: Loguru (configurado via LOG_LEVEL do .env)
- Variáveis de ambiente: python-dotenv (falha silenciosa se .env não existir)
- Porta configurável via APP_PORT no .env (default 8000)

### Frontend (`frontend/`)

- Framework: Streamlit
- Gráficos: Plotly
- Comunicação com backend via `requests` usando BACKEND_API_URL do .env
- Porta configurável via STREAMLIT_SERVER_PORT no .env (default 8501)

### Estrutura de Pastas

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # App FastAPI, startup, health check
│   ├── database.py        # Engine SQLModel, get_session
│   └── models/            # Entidades SQLModel (table=True)
│       └── __init__.py    # Exporta todos os modelos
├── tests/
├── docs/
├── pyproject.toml
└── .python-version        # 3.12

frontend/
├── src/
│   ├── __init__.py
│   └── app.py             # App Streamlit
├── tests/
├── docs/
├── pyproject.toml
└── .python-version        # 3.12
```

## Banco de Dados

### SQLModel — Regras para Modelos

- Criar modelos em `backend/src/models/` (um arquivo por domínio)
- Exportar no `backend/src/models/__init__.py`
- Importar no `main.py` para registrar no metadata
- Sempre criar schemas separados: `ModelCreate` (request) e `ModelRead` (response) sem `table=True`
- Usar `Field(primary_key=True)` com `default=None` para autoincrement
- Usar `Field(index=True)` em campos usados em buscas frequentes
- Usar `Relationship` para relacionamentos entre tabelas
- Tabelas são criadas automaticamente no startup via `create_db_and_tables()`

### ChromaDB

- Modo embedded (biblioteca Python, sem servidor Docker)
- Dados salvos em `CHROMADB_PATH` (default `./chroma_data`)
- Usado para armazenar embeddings de commits, PRs e issues

## Gerenciamento de Dependências (uv)

- SEMPRE usar `uv add` para adicionar dependências (nunca pip install)
- SEMPRE usar `uv add --dev` para dependências de desenvolvimento
- SEMPRE usar `uv run` para executar código e ferramentas
- SEMPRE commitar `uv.lock` no repositório
- NUNCA usar `pip`, `python -m venv`, `poetry` ou `requirements.txt`
- Após qualquer alteração: `uv sync`

## Git e Branches

### Branches

- `main` — código estável, produção. NUNCA commitar direto
- `develop` — integração contínua de features
- `feature/<nome>` — nova funcionalidade (origem: develop, destino: develop)
- `release/<versao>` — preparação de versão (destino: main + develop)
- `hotfix/<nome>` — correções urgentes (origem: main, destino: main + develop)

### Commits Semânticos (OBRIGATÓRIO)

Formato: `tipo: descrição curta`

Tipos permitidos:
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `refactor`: melhoria sem alteração de comportamento
- `test`: testes
- `chore`: tarefas internas

### Pull Requests

- Todo código entra via PR — NUNCA merge direto
- Título claro, descrição com: o que foi feito, por que, como testar
- PR deve ser revisado antes do merge

## Código

- Python 3.12
- PEP 8 via Ruff: `target-version = "py312"`, `line-length = 88`, `select = ["E", "F", "W", "I"]`
- Docstrings em todas as funções e classes públicas
- Testes unitários para toda funcionalidade nova (pytest)
- Testes de propriedade com hypothesis quando aplicável
- Variáveis sensíveis NUNCA no código — sempre via .env
- `.gitignore` deve excluir: `.env`, `.venv/`, `__pycache__/`, `*.db`, `*.sqlite`, `*.sqlite3`, `chroma_data/`, `.hypothesis/`

## Privacidade e Segurança

- Todo processamento acontece localmente
- Nenhum dado pessoal é transmitido externamente
- Tokens e credenciais ficam apenas no `.env` (nunca commitados)
- `.env.example` documenta variáveis com placeholders descritivos

## Referências

- #[[file:fluxograma_dashboard_produtividade.md]]
- #[[file:.kiro/docs-iniciais/dashboard-de-produtividade-dev.md]]
- #[[file:.kiro/docs-iniciais/PRD-dashboard-produtividade-dev.md]]
- #[[file:.kiro/docs-iniciais/gitflow_kiro_guidelines.md]]
- #[[file:.kiro/docs-iniciais/uv_kiro_guidelines.md]]
