# Requisitos — Export e Deploy

## Requisito 1: Export CSV
WHEN o usuário clicar em "Exportar CSV" no dashboard
THE SYSTEM SHALL gerar um arquivo CSV com os dados de métricas do período selecionado e iniciar o download.

### Critérios de Aceitação
- Endpoint `GET /export/csv` retorna arquivo com Content-Type `text/csv`
- CSV inclui colunas: data, commits, PRs abertos, PRs fechados, issues
- Aceita query params `from` e `to` para filtrar período
- Botão no frontend dispara download direto

## Requisito 2: Export PDF
WHEN o usuário clicar em "Exportar PDF" no dashboard
THE SYSTEM SHALL gerar um relatório PDF com KPIs, gráficos e último insight RAG.

### Critérios de Aceitação
- Endpoint `GET /export/pdf` retorna arquivo com Content-Type `application/pdf`
- PDF inclui: título, período, KPIs, resumo de atividade
- Botão no frontend dispara download direto

## Requisito 3: CI/CD backend
WHEN um push for feito no repositório
THE SYSTEM SHALL executar pipeline de lint (ruff) e testes (pytest) via GitHub Actions.

### Critérios de Aceitação
- Workflow roda em push para `develop` e `main`
- Falha no lint ou teste bloqueia o merge
- Usa `uv` para instalar dependências e rodar comandos

## Requisito 4: CI/CD frontend
WHEN um push for feito no repositório
THE SYSTEM SHALL executar pipeline de build e lint no frontend via GitHub Actions.

### Critérios de Aceitação
- Workflow roda em push para `develop` e `main`
- Falha no build ou lint bloqueia o merge
- Usa `npm ci` para instalar dependências

## Requisito 5: Deploy frontend
WHEN um merge for feito na branch `main`
THE SYSTEM SHALL fazer deploy automático do frontend no Vercel.

### Critérios de Aceitação
- Vercel configurado com `VITE_API_URL` apontando para o backend em produção
- Deploy automático via integração GitHub do Vercel
- Preview deploys em PRs

## Requisito 6: Deploy backend
WHEN um merge for feito na branch `main`
THE SYSTEM SHALL fazer deploy automático do backend no Railway.

### Critérios de Aceitação
- Railway configurado com todas as variáveis de ambiente (GITHUB_TOKEN, LLM_PROVIDER, etc.)
- Health check em `GET /health` configurado
- Deploy automático via integração GitHub do Railway
