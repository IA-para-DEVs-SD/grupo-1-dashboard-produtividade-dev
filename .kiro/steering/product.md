---
description: PRD macro do produto — contexto permanente do produto
inclusion: always
---

# Visão Geral do Produto

## Nome do Produto
Dashboard Produtividade Dev

## Propósito
Analisar a produtividade de desenvolvedores a partir de dados reais do GitHub (commits, PRs, issues) e gerar insights personalizados via IA usando RAG (Retrieval-Augmented Generation), permitindo perguntas em linguagem natural sobre padrões de trabalho.

## Usuários-Alvo
- Desenvolvedor individual — quer entender seus padrões de produtividade, picos de performance e áreas de foco
- Tech lead — quer visibilidade sobre ritmo da equipe e identificar gargalos

## Principais Dores
- Dados de produtividade no GitHub são dispersos e difíceis de interpretar manualmente
- Não existe forma simples de cruzar commits, PRs e issues para extrair padrões
- Relatórios manuais consomem tempo e são subjetivos
- Ferramentas existentes não oferecem insights contextuais via linguagem natural

## Features Principais
- Ingestão automática de dados do GitHub via GraphQL API (commits, PRs, issues — últimos 90 dias)
- Pipeline RAG com embeddings (HuggingFace MiniLM) + ChromaDB + LLM (aisuite)
- Chat em linguagem natural para perguntas sobre produtividade
- Dashboard com gráficos (Chart.js) e KPIs ao vivo
- Export de relatórios (CSV/PDF)

## Objetivos de Negócio
- Transformar dados brutos do GitHub em insights acionáveis sem esforço manual
- Oferecer uma ferramenta de auto-análise para devs que valorizam dados
- Demonstrar aplicação prática de RAG + embeddings em contexto real

## Métricas de Sucesso
- Usuário consegue fazer uma pergunta e receber insight relevante em < 10 segundos
- Dashboard exibe KPIs atualizados automaticamente (cron 2x/dia)
- Pipeline RAG retorna chunks relevantes (top-5) com precisão > 80%
- Zero dados pessoais transmitidos externamente (processamento 100% local)

## Limites do Escopo
- Apenas GitHub como fonte de dados (sem GitLab, Bitbucket)
- Single-user (sem multi-tenant / autenticação de equipe)
- Sem billing ou monetização
- Sem app mobile nativo
