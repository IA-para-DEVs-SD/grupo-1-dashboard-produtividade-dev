# Prompts — Dashboard Produtividade Dev

Este documento contém todos os prompts utilizados para criar o projeto usando KiroRails.

---

## 1. Prompt Inicial — Definição do Projeto

```
Crie um dashboard de produtividade para desenvolvedores que:
- Conecta com GitHub via GraphQL API
- Coleta commits, PRs e issues dos últimos 90 dias
- Gera embeddings dos dados e armazena no ChromaDB
- Permite perguntas em linguagem natural via RAG (Retrieval-Augmented Generation)
- Exibe KPIs, gráficos e chat com insights gerados por IA
- Stack: Python/FastAPI (backend), React/Vite (frontend), ChromaDB, HuggingFace MiniLM, aisuite (Ollama/OpenAI)
```

---

## 2. Prompt — Estrutura KiroRails

```
Use KiroRails para organizar o projeto:
- Crie .kiro/steering/ com product.md, tech.md, structure.md
- Crie specs por feature: github-ingestion, rag-pipeline, dashboard-frontend, export-deploy
- Cada spec deve ter: requirements.md (notação EARS), design.md, tasks.md
- Documentação em português
- Use `uv` para Python (nunca pip direto)
- GitFlow: branch feature/kirorails
- NÃO faça commits sem eu pedir
```

---

## 3. Prompt — Feature: Ingestão GitHub

```
Implemente a feature de ingestão de dados do GitHub:
- Modelos Pydantic: Commit, PullRequest, Issue com to_chunk()
- GitHubCollector com GraphQL queries
- Paginação com cursor para volumes > 100
- Endpoint GET /github/status
- Tratamento de erros e logging com loguru
```

---

## 4. Prompt — Feature: Pipeline RAG

```
Implemente o pipeline RAG:
- EmbeddingService com HuggingFace MiniLM (384D)
- VectorStore wrapper para ChromaDB
- LLMClient via aisuite (ollama:llama3.1 ou openai:gpt-4o-mini)
- RAGPipeline: embed query → busca vetorial → prompt → LLM → Insight
- Endpoint POST /insights
- Cron de ingestão 2x/dia com APScheduler
```

---

## 5. Prompt — Feature: Dashboard Frontend

```
Implemente o frontend React:
- Layout com Header, Sidebar, MainLayout
- KPICards consumindo GET /metrics
- Gráficos Chart.js: CommitsChart (barras), PRsChart (linhas)
- ChatPanel para interação RAG
- DateRangePicker para filtro de datas
- MetricToggle para mostrar/ocultar métricas
- ExportButtons para CSV/PDF
```

---

## 6. Prompt — Feature: Export e Deploy

```
Implemente export e deploy:
- GET /export/csv com StreamingResponse
- GET /export/pdf com fpdf2
- CI/CD: backend-ci.yml (ruff + pytest), frontend-ci.yml (build)
- vercel.json para frontend
- Procfile para Railway
```

---

## 7. Prompt — Melhorias de Paginação e Metadados

```
Melhore a ingestão:
- Paginação GraphQL com cursor (5 páginas × 100 itens)
- Metadados no ChromaDB: tipo, data, repositório, autor
- Singleton para EmbeddingService, VectorStore, LLMClient
- MetricsService com filtro de datas, tempo médio merge, hot repos
- Endpoint GET /metrics/weekly para gráficos
- Endpoint POST /ingest para ingestão manual
```

---

## 8. Prompt — Navegação e Configurações

```
Adicione navegação funcional:
- Sidebar com links clicáveis: Dashboard, Chat RAG, Configurações
- Página dedicada para Chat RAG
- Página de Configurações com:
  - Formulário para GITHUB_TOKEN e GITHUB_USERNAME
  - Botão de ingestão manual
  - Painel de status com logs em tempo real
```

---

## 9. Prompt — Status da Ingestão em Tempo Real

```
Quando clicar em "Executar Ingestão", mostre um painel ao lado com:
- Status atual (Executando, Concluído, Erro)
- Etapa atual (Coletando commits, PRs, issues, Gerando embeddings, etc.)
- Logs em tempo real
- Polling a cada 1 segundo
```

---

## 10. Prompt — Instalação do Ollama

```
Instale o Ollama para o Chat RAG funcionar:
- curl -fsSL https://ollama.ai/install.sh | sh
- ollama pull llama3.1
- Timeout de 120s para modelos locais
```

---

## 11. Prompt — Atualização da Documentação

```
Atualize a documentação .kiro:
- Marque todos os requisitos como concluídos nos requirements.md
- Marque todas as tarefas como concluídas nos tasks.md
- Crie prompt.md com todos os prompts usados no projeto
```

---

## 12. Prompt — Implementar Melhorias

```
Implemente todas as recomendações:
- Criar testes unitários para models.py e pipeline.py
- Implementar health check completo (ChromaDB, Ollama, GitHub)
- Persistir configurações em .env
- Adicionar rate limiting nos endpoints
- Implementar cache de métricas
- Melhorar error handling com mensagens específicas
- Validação de formato do GitHub token
```

---

## Prompt do RAG (usado internamente)

O prompt enviado ao LLM para gerar insights:

```python
PROMPT_TEMPLATE = """Você é um assistente de produtividade para desenvolvedores.
Com base nos seguintes dados reais do GitHub do usuário:

{chunks}

Responda à pergunta: {query}

Responda APENAS em JSON válido com este formato (sem markdown, sem ```):
{{"summary": "resposta curta", "evidence": "dados", "recommendation": "sugestão"}}
"""
```

---

## Resumo dos Comandos Executados

```bash
# Backend
cd backend
uv sync
uv add pytest-asyncio slowapi --dev
uv run ruff check .
uv run pytest tests/ -v
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
npx vite build
npx tsc --noEmit

# Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1
```

---

## Estrutura Final do Projeto

```
dashboard-produtividade-dev/
├── .kiro/
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── structure.md
│   ├── specs/
│   │   ├── github-ingestion/    # 8 requisitos, 12 tarefas
│   │   ├── rag-pipeline/        # 12 requisitos, 17 tarefas
│   │   ├── dashboard-frontend/  # 9 requisitos, 18 tarefas
│   │   └── export-deploy/       # 6 requisitos, 8 tarefas
│   └── prompts.md
├── backend/
│   ├── src/
│   │   ├── config.py
│   │   ├── main.py              # Rate limiter configurado
│   │   ├── github/
│   │   ├── rag/
│   │   ├── services/            # Cache de métricas
│   │   └── routes/              # Rate limiting, health detailed
│   ├── tests/
│   │   ├── test_models.py       # 8 testes
│   │   └── test_pipeline.py     # 5 testes
│   ├── pyproject.toml
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   └── vercel.json
├── .github/workflows/
└── README.md
```

## Métricas do Projeto

| Métrica | Valor |
|---------|-------|
| Requisitos totais | 35 |
| Tarefas totais | 55 |
| Testes unitários | 13 |
| Endpoints API | 12 |
| Componentes React | 12 |
| Páginas | 3 |

