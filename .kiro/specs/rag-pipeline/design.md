# Design — Pipeline RAG

## Visão Geral
Pipeline completo de Retrieval-Augmented Generation: recebe chunks de texto do GitHub, gera embeddings, armazena no ChromaDB, e responde perguntas do usuário com insights gerados por LLM.

## Componentes

### EmbeddingService (`backend/src/rag/embeddings.py`)
- Carrega modelo `sentence-transformers/all-MiniLM-L6-v2` (384D)
- Métodos: `embed(text) -> list[float]`, `embed_batch(texts) -> list[list[float]]`
- Modelo carregado uma vez na inicialização (singleton)

### VectorStore (`backend/src/rag/vector_store.py`)
- Wrapper sobre ChromaDB client
- Config: `CHROMA_PATH` (diretório local), `CHROMA_COLLECTION` (nome da collection)
- Métodos: `upsert(id, vector, metadata)`, `query(vector, top_k=5) -> list[Chunk]`
- Usa `PersistentClient` para persistência em disco

### LLMClient (`backend/src/rag/llm_client.py`)
- Usa `aisuite` para abstração de provider
- Config: `LLM_PROVIDER` (ollama/openai), `LLM_MODEL` (llama3.1/gpt-4o-mini)
- Método: `complete(prompt) -> str`

### RAGPipeline (`backend/src/rag/pipeline.py`)
- Orquestra: EmbeddingService + VectorStore + LLMClient
- Método principal: `query(user_input) -> Insight`
- Fluxo interno:
  1. `embedder.embed(user_input)` → vetor da query
  2. `store.query(vetor, top_k=5)` → chunks relevantes
  3. `build_prompt(chunks, user_input)` → prompt formatado
  4. `llm.complete(prompt)` → texto raw
  5. Parsear resposta → `Insight`

### Modelo Insight (`backend/src/rag/models.py`)
```python
class Insight(BaseModel):
    summary: str
    evidence: str
    recommendation: str
    sources: list[str]
```

### Serviço de Ingestão (`backend/src/services/ingestion.py`)
- Background task do FastAPI (`BackgroundTasks` ou `asyncio.create_task`)
- Fluxo: `GitHubCollector.fetch_all()` → `to_chunk()` → `EmbeddingService.embed_batch()` → `VectorStore.upsert()`
- Agendamento via `apscheduler` ou loop simples com `asyncio.sleep`

### Rota de Insights (`backend/src/routes/insights.py`)
- `POST /insights` — recebe `{"query": "..."}`, retorna `Insight`

## Template do Prompt

```
Você é um assistente de produtividade para desenvolvedores.
Com base nos seguintes dados reais do GitHub do usuário:

{chunks}

Responda à pergunta: {query}

Formate sua resposta com:
- Resumo: resposta direta e curta
- Evidência: dados específicos que sustentam a resposta
- Recomendação: sugestão acionável para o desenvolvedor
```

## Decisões Técnicas
- **MiniLM em vez de modelos maiores**: 384D é suficiente para similaridade semântica, roda rápido localmente
- **ChromaDB local**: zero custo, sem dependência externa, ~50MB para 10k vetores
- **aisuite**: troca de provider com uma variável de ambiente, sem mudar código
- **Prompt estruturado**: força o LLM a retornar nos 3 campos esperados

## Dependências
- `sentence-transformers` — embeddings
- `chromadb` — vector store
- `aisuite` — abstração de LLM
