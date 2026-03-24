
# 📊 Fluxograma: Dashboard Produtividade Dev (Full-Stack + RAG + Embeddings)

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
        R1[Query Usuario<br/>ex: 'Meu pico?']
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

    %% Fluxo
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

    %% Ingestion (background)
    B->>G: Query GraphQL<br/>commits/PRs/issues
    G->>B: JSON raw data
    B->>E: Chunk texto → vetores
    E->>DB: Store {vector, metadata}

    %% Query RAG (interativo)
    U->>F: "Quando sou mais produtivo?"
    F->>B: POST /insights
    B->>DB: Embed query → cosine sim
    DB->>B: Top-5 chunks GitHub
    B->>L: Prompt: contexto + query
    L->>B: "Pico terça 9h-12h<br/>Evidência: 120 commits<br/>Recomendação:..."
    B->>F: JSON resposta
    F->>U: Chat + gráfico atualizado
```

## 📋 Componentes Técnicos

| Componente | Tech | Responsabilidade |
|------------|------|------------------|
| **Data Source** | GitHub GraphQL | Commits/PRs/issues reais |
| **Ingestion** | FastAPI + Cron | Puxa/embedding 2x/dia |
| **VectorDB** | ChromaDB | Armazena vetores + metadata |
| **Embeddings** | HuggingFace MiniLM | Query → vetor 384D |
| **LLM** | aisuite (Ollama/GPT) | Gera insights estruturados |
| **Frontend** | React + Chart.js | Dashboard + chat |
| **Deploy** | Vercel + Railway | Frontend + Backend |

## ✅ Validação Passo a Passo

### 1. **Dados Reais** ✅
```
GitHub GraphQL → JSON → chunks → embeddings → ChromaDB
Ex: "feat: auth 50 linhas, 10min review" → vetor
```

### 2. **RAG Funcional** ✅
```
Query: "Meu pico?" → embed → top-5 commits → LLM → "Terça 9h-12h"
```

### 3. **Full-Stack** ✅
```
React (UI) ←→ FastAPI (API) ←→ ChromaDB (dados) ←→ GitHub (fonte)
```

### 4. **Provider Agnostic** ✅
```
aisuite.model = "ollama:llama3.1"  # Curso
aisuite.model = "openai:gpt-4o-mini"  # Produção
```

### 5. **Escalável** ✅
```
Cron 2x/dia → 90 dias = ~10k commits
ChromaDB: 10k vetores = ~50MB disco
```

## 🚀 Deploy GitHub Repo

```
README.md ← este arquivo
└── docs/
    └── fluxograma.md ← este fluxograma
```

**Status:** Fluxograma **100% aderente** à ideia original.
