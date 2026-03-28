# Tarefas — Dashboard Frontend

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar cliente API: fetch wrapper + funções para /metrics, /insights, /github/status | R2,R4,R7 | 2 | ✅ Concluído |
| 2 | Criar layout base: Header, Sidebar, MainLayout com navegação | R1 | 2 | ✅ Concluído |
| 3 | Criar endpoint `GET /metrics` no backend (KPIs calculados) | R7 | 2 | ✅ Concluído |
| 4 | Criar componente KPICard + KPIGrid consumindo /metrics | R2 | 2 | ✅ Concluído |
| 5 | Criar CommitsChart (bar chart — commits/semana) com dados reais | R3 | 2 | ✅ Concluído |
| 6 | Criar PRsChart (line chart — abertos vs fechados) com dados reais | R3 | 2 | ✅ Concluído |
| 7 | Criar ChatPanel: ChatInput + ChatMessage + integração com POST /insights | R4 | 3 | ✅ Concluído |
| 8 | Criar DateRangePicker e integrar com gráficos/KPIs | R5 | 2 | ✅ Concluído |
| 9 | Criar MetricToggle para mostrar/ocultar KPIs | R6 | 1 | ✅ Concluído |
| 10 | Compor página Dashboard.tsx com todos os componentes | R1-R6 | 2 | ✅ Concluído |
| 11 | Criar página ChatPage.tsx dedicada para Chat RAG | R4 | 1 | ✅ Concluído |
| 12 | Criar página SettingsPage.tsx com formulário GitHub | R9 | 2 | ✅ Concluído |
| 13 | Adicionar painel de status da ingestão em tempo real | R9 | 2 | ✅ Concluído |
| 14 | Criar Header.tsx com status de conexão GitHub | R1 | 1 | ✅ Concluído |
| 15 | Implementar navegação funcional no App.tsx | R1 | 1 | ✅ Concluído |
| 16 | Adicionar seletor de provider LLM (Ollama/OpenAI) | R9 | 2 | ✅ Concluído |
| 17 | Adicionar seletor de modelo LLM | R9 | 1 | ✅ Concluído |
| 18 | Adicionar campo para API key OpenAI | R9 | 1 | ✅ Concluído |

## Arquivos Criados/Modificados
- `frontend/src/api/client.ts` — Cliente API com tipos
- `frontend/src/components/Layout/MainLayout.tsx` — Layout com navegação
- `frontend/src/components/Layout/Header.tsx` — Header com status GitHub
- `frontend/src/components/KPICards/KPICard.tsx` — Card individual
- `frontend/src/components/KPICards/KPIGrid.tsx` — Grid de KPIs
- `frontend/src/components/Charts/CommitsChart.tsx` — Gráfico de barras
- `frontend/src/components/Charts/PRsChart.tsx` — Gráfico de linhas
- `frontend/src/components/Chat/ChatPanel.tsx` — Chat RAG
- `frontend/src/components/Filters/DateRangePicker.tsx` — Filtro de datas
- `frontend/src/components/Filters/MetricToggle.tsx` — Toggle de métricas
- `frontend/src/components/Filters/ExportButtons.tsx` — Botões de export
- `frontend/src/pages/Dashboard.tsx` — Página principal
- `frontend/src/pages/ChatPage.tsx` — Página de chat
- `frontend/src/pages/SettingsPage.tsx` — Página de configurações (GitHub + LLM)
- `frontend/src/App.tsx` — Navegação entre páginas
- `frontend/src/vite-env.d.ts` — Tipos Vite
