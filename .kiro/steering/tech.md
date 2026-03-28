---
description: Stack técnica — linguagem, frameworks, banco, build, deploy
inclusion: always
---

# Diretrizes Técnicas

## Linguagem e runtime
- Python 3.11+ (backend)
- Node.js 18+ / TypeScript (frontend)

## Frameworks
- **Backend**: FastAPI 0.110+ (API REST async + cron de ingestão)
- **Frontend**: React 18+ com Vite
- **Gráficos**: Chart.js
- **Orquestração LLM**: aisuite (provider-agnostic — Ollama / OpenAI)
- **RAG**: LangChain (opcional) ou pipeline customizado
- **Logging**: loguru

## Banco de dados
- **ChromaDB** — vector store para embeddings + metadados
- **SQLite** — persistência leve para dados não-vetoriais
- Migrações gerenciadas por Alembic (se necessário SQL)
- Todas as alterações DDL passam por scripts de migração

## Embeddings e LLM
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (384D)
- **LLM dev**: Ollama com `llama3.1` (local, custo zero)
- **LLM prod**: OpenAI `gpt-4o-mini` via aisuite
- **Busca vetorial**: cosine similarity, top-5 chunks

## Build e empacotamento
- **Backend**: `uv` (gerenciador obrigatório — ver uv_kiro_guidelines.md)
  - `uv sync` para instalar dependências
  - `uv run` para executar qualquer comando Python
  - Dependências declaradas em `pyproject.toml`
- **Frontend**: npm
  - `npm install` + `npm run dev` / `npm run build`
- Fixar todas as versões de dependências explicitamente
- Builds de CI devem ser reproduzíveis

## Deploy
- **Frontend**: Vercel
- **Backend**: Railway
- CI/CD via GitHub Actions
- Ambientes: dev → staging → produção
- Endpoint de health check: `GET /health`

## Monitoramento
- Logging estruturado com loguru + correlation IDs
- Endpoint de health check
- Alertas em picos de taxa de erro e degradação de latência

## Fonte de dados
- GitHub GraphQL API
- Dados: commits, PRs, issues, contribuições (últimos 90 dias)
- Autenticação via GitHub Personal Access Token (`read:user` + `repo`)
