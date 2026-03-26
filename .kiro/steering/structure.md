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
│   │   ├── main.py                 # App FastAPI + CORS + rotas
│   │   ├── config.py               # Pydantic Settings (.env)
│   │   ├── github/
│   │   │   ├── collector.py        # GitHubCollector (GraphQL)
│   │   │   └── models.py           # Commit, PullRequest, Issue
│   │   ├── rag/
│   │   │   ├── embeddings.py       # EmbeddingService (MiniLM)
│   │   │   ├── vector_store.py     # VectorStore (ChromaDB)
│   │   │   ├── llm_client.py       # LLMClient (aisuite)
│   │   │   ├── pipeline.py         # RAGPipeline
│   │   │   └── models.py           # Insight
│   │   ├── routes/
│   │   │   ├── health.py           # GET /health
│   │   │   ├── github.py           # GET /github/status
│   │   │   ├── insights.py         # POST /insights
│   │   │   ├── metrics.py          # GET /metrics
│   │   │   └── export.py           # GET /export/csv, /export/pdf
│   │   └── services/
│   │       ├── ingestion.py        # Cron de ingestão (background)
│   │       └── metrics.py          # Cálculo de KPIs
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api/                    # Cliente HTTP para o backend
│   │   ├── components/
│   │   │   ├── Layout/             # Header, Sidebar
│   │   │   ├── Charts/             # Gráficos Chart.js
│   │   │   ├── KPICards/           # Cards de métricas
│   │   │   ├── Chat/               # Chat RAG
│   │   │   └── Filters/            # Filtros de data e métricas
│   │   └── pages/
│   │       └── Dashboard.tsx
│   ├── tests/
│   ├── package.json
│   └── .env.example
├── scripts/                        # Scripts auxiliares
├── .github/
│   └── workflows/                  # CI/CD GitHub Actions
├── .kiro/
│   ├── steering/                   # Contexto permanente do produto
│   │   ├── product.md              # PRD macro
│   │   ├── tech.md                 # Stack técnica
│   │   └── structure.md            # Este arquivo
│   └── specs/                      # Specs por feature
│       ├── backlog.md
│       ├── github-ingestion/
│       ├── rag-pipeline/
│       ├── dashboard-frontend/
│       └── export-deploy/
└── README.md
```

## Responsabilidades por Camada

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| API | `backend/src/routes/` | Endpoints REST — recebe requests, delega para services |
| Serviços | `backend/src/services/` | Lógica de negócio — ingestão, cálculo de KPIs |
| GitHub | `backend/src/github/` | Coleta de dados via GraphQL API |
| RAG | `backend/src/rag/` | Embeddings, vector store, LLM, pipeline completo |
| Frontend | `frontend/src/components/` | Componentes React — gráficos, chat, filtros |
| Config | `backend/src/config.py` | Variáveis de ambiente centralizadas |

## Convenções

- Backend segue PEP 8, linting com ruff
- Frontend em TypeScript com React 18
- Dependências backend gerenciadas com `uv` (nunca pip direto)
- Dependências frontend gerenciadas com npm
- Testes em `tests/` espelhando a estrutura de `src/`
