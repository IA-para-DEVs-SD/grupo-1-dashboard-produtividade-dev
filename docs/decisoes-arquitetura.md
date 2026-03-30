# Decisões de Arquitetura — Dashboard Produtividade Dev

Registro das decisões técnicas tomadas no projeto e suas justificativas.

---

## ADR-001: ChromaDB embedded como vector store

**Contexto:** O projeto precisa de um banco vetorial para armazenar embeddings de commits, PRs e issues do GitHub.

**Decisão:** Usar ChromaDB em modo embedded (PersistentClient), sem servidor separado.

**Justificativa:**
- Zero infraestrutura adicional — roda no mesmo processo do backend
- Persistência em disco via SQLite interno
- API simples para upsert/query com cosine similarity
- Suficiente para single-user com ~10k documentos

**Alternativas consideradas:**
- FAISS: mais rápido, mas sem persistência nativa e sem metadados
- Pinecone/Weaviate: requerem servidor externo, custo, complexidade desnecessária

---

## ADR-002: aisuite como orquestrador LLM (provider-agnostic)

**Contexto:** O projeto precisa suportar LLM local (Ollama) em dev e LLM cloud (OpenAI) em produção.

**Decisão:** Usar aisuite com interface OpenAI-compatible para ambos os providers.

**Justificativa:**
- Troca de provider via variável de ambiente (LLM_PROVIDER)
- Ollama expõe API compatível com OpenAI (/v1/chat/completions)
- Sem lock-in — mesmo código funciona com qualquer provider
- Custo zero em desenvolvimento (Ollama local)

**Alternativas consideradas:**
- LangChain: muito pesado para o caso de uso, abstração desnecessária
- Chamadas diretas à API: duplicação de código entre providers

---

## ADR-003: all-MiniLM-L6-v2 para embeddings

**Contexto:** Precisamos de um modelo de embeddings para transformar texto (commits, PRs, issues) em vetores.

**Decisão:** Usar `all-MiniLM-L6-v2` via sentence-transformers (384 dimensões).

**Justificativa:**
- Modelo leve (~80MB) — carrega rápido, roda em CPU
- 384 dimensões — bom equilíbrio entre qualidade e performance
- Amplamente testado para semantic similarity
- Funciona bem com textos curtos (mensagens de commit, títulos de PR)

**Alternativas consideradas:**
- multilingual-e5-large: melhor qualidade, mas ~2GB e muito lento em CPU
- OpenAI text-embedding-3-small: requer API key e custo por request

---

## ADR-004: Pipeline RAG customizado (sem LangChain)

**Contexto:** O projeto precisa de um pipeline RAG para responder perguntas sobre produtividade.

**Decisão:** Implementar pipeline customizado com 4 componentes: EmbeddingService → VectorStore → LLMClient → RAGPipeline.

**Justificativa:**
- Controle total sobre cada etapa do pipeline
- Sem dependências pesadas (LangChain adiciona ~50 dependências transitivas)
- Código simples e auditável (~100 linhas no total)
- Fácil de testar unitariamente (cada componente é independente)

---

## ADR-005: SQLModel para persistência relacional

**Contexto:** Dados não-vetoriais (configurações, cache) precisam de persistência leve.

**Decisão:** Usar SQLModel (SQLAlchemy + Pydantic unificados) com SQLite.

**Justificativa:**
- Modelos Pydantic e SQLAlchemy no mesmo objeto — menos boilerplate
- SQLite não requer servidor — arquivo local
- Integração nativa com FastAPI (dependency injection via get_session)

---

## ADR-006: Monorepo com subprojetos independentes

**Contexto:** O projeto tem backend (FastAPI) e frontend (Streamlit) com dependências diferentes.

**Decisão:** Monorepo com `backend/` e `frontend/` como subprojetos Python independentes, cada um com seu `pyproject.toml` e `.venv`.

**Justificativa:**
- Isolamento de dependências (FastAPI não precisa do Streamlit e vice-versa)
- CI independente por subprojeto (path filters no GitHub Actions)
- `uv sync` independente — sem conflitos de versão
- Código compartilhado via API HTTP, não via imports diretos
