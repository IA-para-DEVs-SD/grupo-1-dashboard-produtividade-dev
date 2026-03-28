# Tarefas — Pipeline RAG

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar modelo `Insight` (Pydantic: summary, evidence, recommendation, sources) | R7 | 1 | ✅ Concluído |
| 2 | Criar `EmbeddingService` com MiniLM — `embed()` e `embed_batch()` + Singleton | R1 | 3 | ✅ Concluído |
| 3 | Criar `VectorStore` wrapper ChromaDB — `upsert()` e `query()` + Singleton | R2 | 3 | ✅ Concluído |
| 4 | Criar `LLMClient` via aisuite — `complete()` com config de provider + Singleton | R5 | 3 | ✅ Concluído |
| 5 | Implementar serviço de ingestão: coletar → chunk → embed → upsert | R3 | 4 | ✅ Concluído |
| 6 | Implementar prompt builder com template estruturado | R5 | 2 | ✅ Concluído |
| 7 | Criar `RAGPipeline` orquestrando embed → query → prompt → LLM → Insight | R4,R5 | 4 | ✅ Concluído |
| 8 | Criar rota `POST /insights` | R6 | 2 | ✅ Concluído |
| 9 | Configurar cron de ingestão como background task (APScheduler) | R3 | 3 | ✅ Concluído |
| 10 | Criar endpoint `GET /ingest/status` com progresso em tempo real | R8 | 2 | ✅ Concluído |
| 11 | Criar endpoint `POST /ingest` para ingestão manual | R9 | 2 | ✅ Concluído |
| 12 | Aumentar timeout do LLM para 120s (Ollama) | R5 | 1 | ✅ Concluído |
| 13 | Parsing flexível de resposta JSON do LLM | R5,R7 | 2 | ✅ Concluído |
| 14 | Adicionar rate limiting com slowapi | R10 | 2 | ✅ Concluído |
| 15 | Implementar cache in-memory para métricas (TTL 60s) | R11 | 2 | ✅ Concluído |
| 16 | Criar endpoint `GET /health/detailed` | R12 | 2 | ✅ Concluído |
| 17 | Criar testes unitários para RAGPipeline | R7 | 3 | ✅ Concluído |

## Arquivos Criados/Modificados
- `backend/src/rag/models.py` — Modelo Insight
- `backend/src/rag/embeddings.py` — EmbeddingService (Singleton)
- `backend/src/rag/vector_store.py` — VectorStore (Singleton)
- `backend/src/rag/llm_client.py` — LLMClient (Singleton, timeout 120s)
- `backend/src/rag/pipeline.py` — RAGPipeline com parsing flexível
- `backend/src/services/ingestion.py` — Serviço de ingestão com status
- `backend/src/services/metrics.py` — MetricsService com cache
- `backend/src/routes/insights.py` — POST /insights com rate limit
- `backend/src/routes/metrics.py` — GET /ingest/status, POST /ingest com rate limit
- `backend/src/routes/health.py` — GET /health, GET /health/detailed
- `backend/src/main.py` — Configuração do rate limiter
- `backend/tests/test_pipeline.py` — Testes unitários para RAGPipeline
