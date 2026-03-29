---
description: Stack técnica — linguagem, frameworks, banco, build, deploy
inclusion: always
---

# Diretrizes Técnicas

## Linguagem e runtime
- Python 3.12 (backend e frontend)

## Frameworks
- **Backend**: FastAPI 0.115+ (API REST async + cron de ingestão)
- **Frontend**: Streamlit 1.40+
- **Gráficos**: Plotly
- **Rate limiting**: slowapi
- **Orquestração LLM**: aisuite (provider-agnostic — Ollama / OpenAI)
- **RAG**: pipeline customizado
- **Logging**: loguru + correlation IDs

## Banco de dados
- **ChromaDB** — vector store para embeddings + metadados (modo embedded, sem servidor)
- **SQLite** — persistência leve para dados não-vetoriais via SQLModel

## Embeddings e LLM
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (384D) via sentence-transformers
- **LLM dev**: Ollama com `llama3.1` (local, custo zero)
- **LLM prod**: OpenAI `gpt-4o-mini` via aisuite
- **Busca vetorial**: cosine similarity, top-5 chunks

## Build e empacotamento
- **Backend e Frontend**: `uv` (gerenciador obrigatório)
  - `uv sync` para instalar dependências
  - `uv run` para executar qualquer comando Python
  - Dependências declaradas em `pyproject.toml`
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
- Endpoint de health check (`/health` e `/health/detailed`)
- Alertas em picos de taxa de erro e degradação de latência

## Fonte de dados
- GitHub GraphQL API
- Dados: commits, PRs, issues, contribuições (últimos 90 dias)
- Autenticação via GitHub Personal Access Token (`read:user` + `repo`)
