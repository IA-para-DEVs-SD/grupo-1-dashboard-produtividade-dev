---
description: Estrutura do projeto — organização de diretórios e responsabilidades
inclusion: always
---

# Estrutura do Projeto

## Visão Geral

```
dashboard-produtividade-dev/
├── backend/
│   ├── src/
│   │   ├── main.py                 # App FastAPI + CORS + rate limiting + rotas
│   │   ├── config.py               # Pydantic Settings (.env)
│   │   ├── database.py             # Engine SQLModel, get_session
│   │   ├── logging_config.py       # Loguru + correlation IDs
│   │   ├── github/
│   │   │   ├── collector.py        # GitHubCollector (GraphQL)
│   │   │   └── models.py           # Commit, PullRequest, Issue
│   │   ├── rag/
│   │   │   ├── embeddings.py       # EmbeddingService (all-MiniLM-L6-v2)
│   │   │   ├── vector_store.py     # VectorStore (ChromaDB)
│   │   │   ├── llm_client.py       # LLMClient (aisuite)
│   │   │   ├── pipeline.py         # RAGPipeline
│   │   │   └── models.py           # Insight
│   │   ├── routes/
│   │   │   ├── health.py           # GET /health, GET /health/detailed
│   │   │   ├── github.py           # GET /github/status
│   │   │   ├── insights.py         # POST /insights
│   │   │   ├── metrics.py          # GET /metrics, GET /metrics/weekly
│   │   │   ├── export.py           # GET /export/csv, /export/pdf
│   │   │   └── settings.py         # GET/POST /settings/github, /settings/llm
│   │   └── services/
│   │       ├── ingestion.py        # Cron de ingestão (APScheduler, 12h)
│   │       └── metrics.py          # Cálculo de KPIs + cache em memória
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app.py                  # App Streamlit principal (navegação)
│   │   ├── api_client.py           # Cliente HTTP para o backend
│   │   └── pages/
│   │       ├── dashboard.py        # KPIs + gráficos Plotly
│   │       ├── chat.py             # Chat RAG
│   │       └── settings.py         # Configurações GitHub/LLM/Ingestão
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── scripts/                        # Scripts auxiliares
├── .github/
│   └── workflows/                  # CI/CD GitHub Actions
├── .kiro/
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   ├── structure.md
│   │   ├── backend.md
│   │   └── frontend.md
│   └── specs/
└── README.md
```

## Responsabilidades por Camada

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| API | `backend/src/routes/` | Endpoints REST — recebe requests, delega para services |
| Serviços | `backend/src/services/` | Lógica de negócio — ingestão, cálculo de KPIs |
| GitHub | `backend/src/github/` | Coleta de dados via GraphQL API |
| RAG | `backend/src/rag/` | Embeddings, vector store, LLM, pipeline completo |
| Frontend | `frontend/src/` | App Streamlit — dashboard, chat RAG, configurações |
| Config | `backend/src/config.py` | Variáveis de ambiente centralizadas |

## Convenções

- Backend e frontend seguem PEP 8, linting com ruff
- Ambos gerenciados com `uv` (nunca pip direto)
- Testes em `tests/` espelhando a estrutura de `src/`
