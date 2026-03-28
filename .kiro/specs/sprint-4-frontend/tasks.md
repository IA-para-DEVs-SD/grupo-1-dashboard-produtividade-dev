# 🏃 Sprint 4 — Frontend Dashboard

> Objetivo: Dashboard React com gráficos, KPIs, chat RAG e filtros interativos.

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar layout base: header, sidebar, área de conteúdo principal | R19 | 2 | 🔲 A fazer |
| 2 | Criar cliente de API (fetch wrapper) apontando para VITE_API_URL | R19 | 1 | 🔲 A fazer |
| 3 | Endpoint `GET /metrics` — retorna KPIs (commits/dia, PRs/semana, hot files) | R25 | 2 | 🔲 A fazer |
| 4 | Componente de cards KPI: commits/semana, PRs resolvidos, tempo médio merge | R21 | 2 | 🔲 A fazer |
| 5 | Gráfico de commits/semana com Chart.js (gráfico de barras) | R20 | 2 | 🔲 A fazer |
| 6 | Gráfico de PRs abertos vs fechados (gráfico de linhas) | R20 | 2 | 🔲 A fazer |
| 7 | Componente Chat RAG: input + output + estado de carregamento | R22 | 3 | 🔲 A fazer |
| 8 | Integrar chat com `POST /insights` — enviar query, exibir resposta | R22 | 2 | 🔲 A fazer |
| 9 | Filtro de intervalo de datas (seletor de período) | R23 | 2 | 🔲 A fazer |
| 10 | Seletores de métricas (toggle de quais KPIs exibir) | R24 | 1 | 🔲 A fazer |

## Critérios de Conclusão
- Dashboard carrega com layout responsivo
- KPIs exibem dados reais do backend
- Gráficos renderizam com Chart.js
- Chat RAG envia pergunta e exibe resposta do LLM
- Filtros de data e métricas funcionais
