# PRD — Dashboard de Produtividade Dev

**Versão:** 1.0  
**Data:** 25/03/2026  
**Status:** Draft

---

## 1. Visão Geral

O Dashboard de Produtividade Dev é uma aplicação full-stack local-first que coleta dados reais do GitHub, processa com embeddings e responde perguntas em linguagem natural via RAG. O objetivo é dar ao desenvolvedor visibilidade sobre seus próprios padrões de trabalho sem depender de serviços externos pagos.

---

## 2. Problema

Desenvolvedores não têm uma visão consolidada do próprio ritmo de trabalho. Métricas ficam espalhadas no GitHub, sem contexto, sem análise temporal e sem resposta para perguntas como "por que fui menos produtivo em março?" ou "qual meu melhor horário para codar?".

---

## 3. Objetivo do Produto

Fornecer um dashboard interativo + chat RAG que:
- Agrega dados reais do GitHub (commits, PRs, issues, reviews)
- Calcula KPIs de produtividade automaticamente
- Responde perguntas em linguagem natural com base no histórico real
- Gera relatórios semanais automatizados
- Funciona 100% local, sem custo de API

---

## 4. Usuários-Alvo

- Desenvolvedor individual que quer entender seus padrões de produtividade
- Tech lead que quer acompanhar o próprio ritmo antes de reuniões de retrospectiva
- Qualquer dev que usa GitHub como fonte principal de trabalho

---

## 5. Funcionalidades

### 5.1 Coleta e Ingestão de Dados

- Cron job diário (2:00 AM) que puxa via GitHub GraphQL:
  - Commits dos últimos 90 dias
  - PRs abertos/fechados e tempo de merge
  - Issues criados/resolvidos
  - Contribuições por data e repositório
- Cada entrada é transformada em chunk de texto e embeddada com `intfloat/multilingual-e5-large` (HuggingFace, gratuito)
- Vetores 1024D armazenados no ChromaDB com metadados (data, repo, tipo, autor)

### 5.2 Dashboard (Frontend Streamlit)

- Gráficos interativos via Plotly:
  - Commits por semana/dia da semana
  - PRs resolvidos ao longo do tempo
  - Tempo médio de merge
  - Hot files (arquivos mais modificados)
- KPIs em tempo real: commits/dia, PRs abertos, taxa de resolução de issues
- Filtros de intervalo de datas e seletor de repositórios
- Export de relatórios em CSV e PDF

### 5.3 Chat RAG

- Input de linguagem natural no dashboard
- Fluxo: query → embed → cosine similarity top-5 → prompt LLM → resposta contextual
- Exemplos de perguntas suportadas:
  - "Qual meu pico de produtividade?"
  - "Por que refatorei menos em março?"
  - "Quais arquivos eu mais mexi essa semana?"
- LLM: Llama 3.1 8B via Ollama (local, offline)
- Abstração de provider via `aisuite` (troca para GPT-4o-mini sem mudar código)

### 5.4 Relatórios Automatizados

- Relatório semanal gerado pelo LLM com padrões identificados
- Exemplos: "Você é 20% mais lento às sextas", "PRs grandes acumulam no fim da semana"
- Disponível no dashboard e exportável em PDF

---

## 6. Arquitetura

```
GitHub GraphQL
      ↓
FastAPI (Backend)
  ├── Ingestion Cron → HuggingFace Embeddings → ChromaDB
  ├── KPI Calculator → SQLite
  └── RAG Endpoints → aisuite (Ollama/LLM)
      ↓
Streamlit (Frontend)
  ├── Plotly Charts
  ├── Chat RAG
  └── Export PDF/CSV
```

---

## 7. Stack Técnica

| Camada         | Tecnologia                              | Justificativa                              |
|----------------|-----------------------------------------|--------------------------------------------|
| Frontend       | Streamlit + Plotly                      | Prototipagem rápida, dashboards responsivos |
| Backend        | FastAPI + LangChain                     | Async, chains RAG nativas                  |
| VectorDB       | ChromaDB                                | Local, gratuito, integra com metadados SQL |
| Embeddings     | intfloat/multilingual-e5-large (HF)     | Multilingual, offline, vetores 1024D       |
| LLM            | Ollama (Llama 3.1 8B)                   | Offline, custo zero                        |
| LLM Abstração  | aisuite                                 | Provider-agnostic, troca sem refactor      |
| Banco de Dados | SQLite                                  | Persistência leve para KPIs e metadados    |
| Log            | loguru                                  | Logging simples e legível                  |

---

## 8. Requisitos Não-Funcionais

- **Privacidade**: todo processamento local, nenhum dado enviado externamente
- **Performance**: ingestão de 90 dias (~10k commits) em menos de 5 minutos; ChromaDB com 10k vetores ≈ 50MB disco
- **Disponibilidade**: funciona offline após primeira ingestão
- **Portabilidade**: deploy opcional em nuvem com dados criptografados
- **Qualidade de código**: PEP 8, docstrings, testes unitários para novas funcionalidades

---

## 9. Fora do Escopo (v1.0)

- Suporte a múltiplos usuários / multi-tenant
- Integração com Jira, Linear ou outras ferramentas além do GitHub
- App mobile
- Autenticação OAuth completa (v1 usa Personal Access Token)

---

## 10. Critérios de Aceite

| Funcionalidade          | Critério                                                                 |
|-------------------------|--------------------------------------------------------------------------|
| Ingestão                | Cron executa, dados do GitHub aparecem no ChromaDB sem erro              |
| Dashboard               | Gráficos renderizam com dados reais dos últimos 90 dias                  |
| Chat RAG                | Pergunta em PT-BR retorna resposta contextual em < 10s (local)           |
| Relatório semanal       | PDF gerado com pelo menos 3 insights baseados em dados reais             |
| Export                  | CSV e PDF exportados corretamente com dados do período selecionado       |
| Privacidade             | Nenhuma requisição externa além do GitHub API e HuggingFace (download)   |

---

## 11. Referências

- [Fluxograma de Arquitetura](../../fluxograma_dashboard_produtividade.md)
- [Documento de Visão Inicial](./dashboard-de-produtividade-dev.md)
- [aisuite](https://github.com/andrewyng/aisuite)
- [intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)
