# Dashboard de Produtividade Dev

O Dashboard de Produtividade Dev é um app full-stack que puxa dados do GitHub, analisa com IA e gera insights personalizados via RAG (Retrieval-Augmented Generation) + embeddings para consultas naturais.

## Arquitetura Full-Stack

**Frontend**:
Streamlit para dashboard interativo com gráficos (commits/semana, PRs resolvidos, tempo médio de merge), chat para  perguntas como "Por que refatorei menos em março?" e export de relatórios PDF.​​

**Backend**:
FastAPI para orquestrar APIs do GitHub (GraphQL para métricas),  calcular KPIs básicos (commits/dia, hot files) e expor endpoints para o RAG.​​

**Banco/VectorDB**:
 Chroma para armazenar embeddings de histórico de commits/PRs e docs pessoais (READMEs, ADRs).​

## Fluxo RAG + Embeddings

1. **Coleta/Ingestion**:
   Script cron puxa dados via GitHub API (commits, PRs, issues, duração de
   reviews) e embedda textos com o modelo `intfloat/multilingual-e5-large` gratuito do Hugging Face.​​

2. **Embeddings**: Cada entrada (ex.: "Commit X: refatoração auth, 50 linhas") vira vetor **1024D** armazenado com metadados (data, repo, autor).​

3. **Query RAG**:
   Usuário pergunta "Meu pico de produtividade?" → embedda query → busca 
   top-5 docs similares (cosine similarity) → LLM ( `Llama 3.1 8B` 
   via Ollama) gera resposta contextual: "Pico em fev/26: 120 commits, foco
   em feature Y".​​

4. **Insights Automatizados**: LLM gera relatório semanal: "Você é 20% mais lento às sextas; padrão: PRs grandes acumulam em sextas".

## Stack Técnica Recomendada

| Camada            | Techs                                                               | Por quê?                                               |
| ----------------- | ------------------------------------------------------------------- | ------------------------------------------------------ |
| Frontend          | Streamlit + Plotly                                                  | Dashboards responsivos, fáceis de prototipar           |
| Backend           | FastAPI + LangChain                                                 | Rápido para APIs async, chains RAG nativas​            |
| VectorDB          | Chroma                                                              | Local/grátis, integra com SQL para joins em metadados​ |
| LLM/Embed         | Ollama (Llama 3.1 8B) + HuggingFace(intfloat/multilingual-e5-large) | Offline, custo zero para POC​                          |
| Banco de Dados    | SQlite para outras necessidades que não seja vetorial               | Lightweight data persistence                           |
| Provider-agnostic | [aisuite](https://github.com/andrewyng/aisuite)                     | perfeito para abstrair o LLM                           |
| Log               | loguru                                                              | A logging library                                      |

## Diretrizes de Desenvolvimento

- Siga o guia de estilo Python PEP 8
- Adicione docstrings abrangentes
- Inclua testes unitários para novas funcionalidades
- Atualize a documentação para quaisquer alterações

## Privacidade e Segurança

- Todo o processamento de dados acontece localmente
- Nenhuma informação pessoal é transmitida externamente
- Implantação opcional em nuvem com transferência de dados criptografada
- O usuário controla toda a retenção e exclusão de dados

## Funcionalidades do Dashboard

### Análises Principais

- **Tendências de Pontuação de Foco**: Acompanhe padrões de concentração ao longo do tempo
- **Análise de Dependência de IA**: Entenda o impacto do uso de ferramentas de IA
- **Padrões de Densidade de Bugs**: Relacione a qualidade do código com a produtividade
- **Energia vs Desempenho**: Analise a relação com a carga cognitiva

---

### Elementos Interativos

- **Filtros de Intervalo de Datas**: Personalize os períodos de análise
- **Seletores de Métricas**: Escolha KPIs específicos para exibição
- **Opções de Exportação**: Baixe os insights em CSV ou PDF
- **Atualizações em Tempo Real**: Capacidade de atualização contínua dos dados
