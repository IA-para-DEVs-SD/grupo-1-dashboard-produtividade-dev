# Design — Dashboard Frontend

## Visão Geral
Dashboard React com gráficos interativos, KPIs ao vivo, chat RAG e filtros. Consome a API FastAPI do backend.

## Componentes

### Layout (`frontend/src/components/Layout/`)
- `Header.tsx` — nome do produto, status de conexão, avatar
- `Sidebar.tsx` — navegação entre seções
- `MainLayout.tsx` — wrapper com header + sidebar + conteúdo

### KPI Cards (`frontend/src/components/KPICards/`)
- `KPICard.tsx` — card genérico: título, valor, ícone, variação
- `KPIGrid.tsx` — grid de cards consumindo `GET /metrics`

### Gráficos (`frontend/src/components/Charts/`)
- `CommitsChart.tsx` — bar chart (commits/semana) com Chart.js
- `PRsChart.tsx` — line chart (PRs abertos vs fechados)
- Usa `react-chartjs-2` como wrapper

### Chat RAG (`frontend/src/components/Chat/`)
- `ChatInput.tsx` — campo de texto + botão enviar
- `ChatMessage.tsx` — exibe uma mensagem (pergunta ou resposta)
- `ChatPanel.tsx` — painel completo com histórico + input
- Consome `POST /insights`

### Filtros (`frontend/src/components/Filters/`)
- `DateRangePicker.tsx` — seletor de período (início/fim)
- `MetricToggle.tsx` — toggles para mostrar/ocultar métricas

### Cliente API (`frontend/src/api/`)
- `client.ts` — fetch wrapper com base URL de `VITE_API_URL`
- `metrics.ts` — `getMetrics(from?, to?)`
- `insights.ts` — `postInsight(query)`
- `github.ts` — `getGitHubStatus()`

### Página Principal (`frontend/src/pages/`)
- `Dashboard.tsx` — compõe: filtros + KPIs + gráficos + chat

## Decisões Técnicas
- **React 18 + Vite**: build rápido, HMR, TypeScript nativo
- **Chart.js via react-chartjs-2**: leve, boa documentação, suficiente para os gráficos necessários
- **Componentes isolados**: cada componente consome sua própria API, facilita testes e manutenção
- **Estado local (useState/useEffect)**: sem necessidade de state manager global para MVP

## Dependências
- `react`, `react-dom` — framework
- `chart.js`, `react-chartjs-2` — gráficos
- `typescript` — tipagem
