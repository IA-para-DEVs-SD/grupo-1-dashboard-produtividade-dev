# 🏃 Sprint 3 — Pipeline RAG (Embeddings + ChromaDB + LLM)

> Objetivo: Pipeline RAG completo — embeddings, vector store, busca semântica, integração LLM, endpoint /insights.

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar `EmbeddingService` com HuggingFace MiniLM (`all-MiniLM-L6-v2`, 384D) | R11 | 3 | 🔲 A fazer |
| 2 | Criar `VectorStore` wrapper para ChromaDB (collection, upsert, query) | R12 | 3 | 🔲 A fazer |
| 3 | Implementar ingestão completa: chunks → embed → upsert no ChromaDB com metadados | R12,R13 | 4 | 🔲 A fazer |
| 4 | Implementar cron job de ingestão (background task no FastAPI) | R13 | 3 | 🔲 A fazer |
| 5 | Criar `LLMClient` via aisuite (provider-agnostic: ollama/openai) | R15 | 3 | 🔲 A fazer |
| 6 | Criar `RAGPipeline`: embed query → cosine sim top-5 → build prompt → LLM | R14,R16 | 4 | 🔲 A fazer |
| 7 | Criar modelo `Insight` (resumo, evidência, recomendação, fontes) | R18 | 1 | 🔲 A fazer |
| 8 | Implementar prompt builder: template com contexto + query | R16 | 2 | 🔲 A fazer |
| 9 | Criar endpoint `POST /insights` — recebe query, retorna Insight | R17 | 2 | 🔲 A fazer |
| 10 | Teste ponta a ponta: ingestão → query → insight gerado | R14-R18 | 4 | 🔲 A fazer |

## Critérios de Conclusão
- Embeddings gerados corretamente (384D) e armazenados no ChromaDB
- Query RAG retorna top-5 chunks relevantes
- LLM gera insight estruturado com resumo + evidência + recomendação
- `POST /insights` funcional com resposta JSON
- Cron job roda em background sem bloquear API
