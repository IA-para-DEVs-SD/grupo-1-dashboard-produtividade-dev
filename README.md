<div align="center">

# 📊 Dashboard Produtividade Dev

**Full-Stack · RAG · Embeddings · GitHub Analytics**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-8B5CF6?style=for-the-badge)](https://www.trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> Dashboard inteligente que analisa sua produtividade como dev diretamente dos dados reais do GitHub — commits, PRs e issues — com insights gerados por IA via RAG (Retrieval-Augmented Generation).

</div>

---

## 🎯 Sobre o Projeto

O **Dashboard Produtividade Dev** conecta sua conta GitHub e transforma dados brutos de contribuições em **insights acionáveis** sobre seus padrões de trabalho. Com uma pipeline RAG alimentada por embeddings reais dos seus commits, você pode perguntar em linguagem natural:

- _"Quando sou mais produtivo durante a semana?"_
- _"Qual foi meu melhor sprint dos últimos 90 dias?"_
- _"Em quais tipos de tarefas gasto mais tempo?"_

---

## 🏗️ Arquitetura Geral

```mermaid
graph TB
    subgraph GitHub["🐙 GitHub API (GraphQL)"]
        G1[Commits<br/>últimos 90d]
        G2[PRs<br/>abertos/fechados]
        G3[Issues<br/>criados/resolvidos]
        G4[Contribuições<br/>por autor/data]
    end

    subgraph Ingestion["🚀 Backend FastAPI"]
        I1[Ingestion Cron<br/>diário 2:00AM]
        I2[Parse JSON<br/>→ chunks texto]
        I3[Embeddings<br/>HuggingFace MiniLM]
        I4[Store ChromaDB<br/>vetores + metadata]
    end

    subgraph RAG["🧠 RAG Pipeline"]
        R1[Query Usuário<br/>ex: 'Meu pico?']
        R2[Embed Query<br/>MiniLM]
        R3[Cosine Similarity<br/>top-5 chunks]
        R4[Prompt LLM<br/>contexto + query]
        R5[aisuite LLM<br/>Llama3.1 / GPT-4o-mini]
        R6[Resposta<br/>Insight estruturado]
    end

    subgraph Frontend["📱 React Dashboard"]
        F1[Gráficos<br/>Chart.js]
        F2[Chat RAG<br/>input/output]
        F3[KPIs Live<br/>commits/semana]
    end

    GitHub --> I1
    I1 --> I2
    I2 --> I3
    I3 --> I4

    F2 --> R1
    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> R5
    R5 --> R6
    R6 --> F2
    R6 --> F3

    classDef github fill:#f1f5f9,stroke:#1f2937,stroke-width:3px,color:#111827
    classDef backend fill:#06b6d4,stroke:#0891b2,stroke-width:3px,color:#fff
    classDef rag fill:#8b5cf6,stroke:#7c3aed,stroke-width:3px,color:#fff
    classDef frontend fill:#10b981,stroke:#059669,stroke-width:3px,color:#fff

    class G1,G2,G3,G4 github
    class I1,I2,I3,I4 backend
    class R1,R2,R3,R4,R5,R6 rag
    class F1,F2,F3 frontend
```

---

## 🔄 Fluxo de Dados Detalhado

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend React
    participant B as Backend FastAPI
    participant DB as ChromaDB
    participant G as GitHub GraphQL
    participant E as Embeddings
    participant L as LLM (aisuite)

    Note over U,F: Dashboard carregado
    Note over F,B: Autentica GitHub Token

    rect rgb(240, 249, 255)
        Note over B,DB: Ingestão (background — cron 2x/dia)
        B->>G: Query GraphQL commits/PRs/issues
        G->>B: JSON raw data
        B->>E: Chunk texto → vetores
        E->>DB: Store {vector, metadata}
    end

    rect rgb(245, 243, 255)
        Note over U,F: Query RAG (interativo)
        U->>F: "Quando sou mais produtivo?"
        F->>B: POST /insights
        B->>DB: Embed query → cosine sim
        DB->>B: Top-5 chunks GitHub
        B->>L: Prompt: contexto + query
        L->>B: "Pico terça 9h-12h · 120 commits"
        B->>F: JSON resposta
        F->>U: Chat + gráfico atualizado
    end
```

---

## 🧩 Diagrama de Classes (Domínio)

> ⚠️ **Diagrama conceitual** — gerado a partir da documentação de arquitetura. Sujeito a revisão conforme implementação do código.

```mermaid
classDiagram
    class GitHubCollector {
        +String token
        +int days_back
        +fetch_commits() List~Commit~
        +fetch_pull_requests() List~PR~
        +fetch_issues() List~Issue~
    }

    class Commit {
        +String sha
        +String message
        +String author
        +DateTime date
        +int additions
        +int deletions
        +to_chunk() String
    }

    class EmbeddingService {
        +String model_name
        +embed(text: String) Vector
        +embed_batch(texts: List) List~Vector~
    }

    class VectorStore {
        +ChromaClient client
        +String collection_name
        +upsert(id, vector, metadata)
        +query(vector, top_k) List~Chunk~
    }

    class RAGPipeline {
        +EmbeddingService embedder
        +VectorStore store
        +LLMClient llm
        +query(user_input: String) Insight
        -build_prompt(chunks, query) String
    }

    class Insight {
        +String summary
        +String evidence
        +String recommendation
        +List~Chunk~ sources
    }

    class LLMClient {
        +String provider
        +String model
        +complete(prompt: String) String
    }

    GitHubCollector --> Commit
    Commit --> EmbeddingService : texto chunk
    EmbeddingService --> VectorStore : vetores
    RAGPipeline --> EmbeddingService
    RAGPipeline --> VectorStore
    RAGPipeline --> LLMClient
    RAGPipeline --> Insight
``` 

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Responsabilidade |
|--------|-----------|------------------|
| **Data Source** | GitHub GraphQL API | Commits, PRs e issues reais |
| **Backend** | FastAPI + Cron | API REST + ingestão agendada |
| **Vector DB** | ChromaDB | Armazenamento de vetores + metadata |
| **Embeddings** | HuggingFace MiniLM (384D) | Transformação texto → vetor |
| **LLM** | aisuite (Ollama / OpenAI) | Geração de insights estruturados |
| **Frontend** | React + Chart.js | Dashboard interativo + chat |
| **Deploy** | Vercel + Railway | Frontend + Backend em produção |

---

## 📁 Estrutura do Projeto

```
dashboard-produtividade-dev/
├── backend/
│   ├── src/            # Código-fonte FastAPI
│   ├── tests/          # Testes unitários e de integração
│   ├── docs/           # Documentação do backend
│   └── .env.example    # Variáveis de ambiente (template)
├── frontend/
│   ├── src/            # Componentes React
│   ├── tests/          # Testes do frontend
│   ├── docs/           # Documentação do frontend
│   └── .env.example    # Variáveis de ambiente (template)
├── scripts/            # Scripts auxiliares (seed, migration, etc.)
├── docs/
│   └── fluxograma_dashboard_produtividade.md
├── .github/            # Workflows CI/CD
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Token GitHub com escopo `read:user` e `repo`
- [Ollama](https://ollama.ai) instalado localmente (para modo dev)

### Backend

```bash
# Clone o repositório
git clone https://github.com/IA-para-DEVs-SD/dashboard-produtividade-dev.git
cd dashboard-produtividade-dev/backend

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite o .env com seu GITHUB_TOKEN e configurações LLM

# Inicie o servidor
uvicorn src.main:app --reload
```

### Frontend

```bash
cd ../frontend

# Instale dependências
npm install

# Configure variáveis de ambiente
cp .env.example .env

# Inicie o servidor de desenvolvimento
npm run dev
```

---

## ⚙️ Variáveis de Ambiente

### Backend (`backend/.env`)

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=seu_usuario

# LLM — escolha o provider
LLM_PROVIDER=ollama          # ou: openai
LLM_MODEL=llama3.1           # ou: gpt-4o-mini

# ChromaDB
CHROMA_PATH=./data/chroma
CHROMA_COLLECTION=github_activity

# Ingestão
INGESTION_DAYS_BACK=90
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=http://localhost:8000
```

---

## ✅ Validações do Sistema

| # | Feature | Fluxo | Status |
|---|---------|-------|--------|
| 1 | **Dados Reais** | GitHub GraphQL → JSON → chunks → embeddings → ChromaDB | ✅ |
| 2 | **RAG Funcional** | Query → embed → top-5 chunks → LLM → insight | ✅ |
| 3 | **Full-Stack** | React ↔ FastAPI ↔ ChromaDB ↔ GitHub | ✅ |
| 4 | **Provider Agnostic** | `ollama:llama3.1` (dev) / `openai:gpt-4o-mini` (prod) | ✅ |
| 5 | **Escalável** | Cron 2x/dia · 90 dias · ~10k commits · ~50MB ChromaDB | ✅ |

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

<div align="center">
Feito com 🧠 + ☕ pela equipe <strong>IA para DEVs SD</strong>
</div>