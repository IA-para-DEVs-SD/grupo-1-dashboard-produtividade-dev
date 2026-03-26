# Requisitos — Dashboard Frontend

## Requisito 1: Layout base
WHEN o usuário acessar o dashboard
THE SYSTEM SHALL exibir um layout responsivo com header, sidebar de navegação e área de conteúdo principal.

### Critérios de Aceitação
- [x] Layout renderiza corretamente em desktop (1280px+) e tablet (768px+)
- [x] Header exibe nome do produto e status de conexão GitHub
- [x] Sidebar permite navegar entre seções (Dashboard, Chat, Configurações)
- [x] Navegação funcional com estado no App.tsx

## Requisito 2: KPIs ao vivo
WHEN o dashboard carregar
THE SYSTEM SHALL exibir cards com KPIs: commits/semana, PRs resolvidos, tempo médio de merge.

### Critérios de Aceitação
- [x] Dado que o backend retorne dados em `GET /metrics`
- [x] Quando o dashboard carregar
- [x] Então deve exibir pelo menos 3 cards com valores numéricos
- [x] E os valores devem refletir os dados reais do backend

## Requisito 3: Gráficos de atividade
WHEN o dashboard carregar
THE SYSTEM SHALL renderizar gráficos de commits/semana (barras) e PRs abertos vs fechados (linhas) usando Chart.js.

### Critérios de Aceitação
- [x] Gráfico de barras mostra commits por semana (últimas 12 semanas)
- [x] Gráfico de linhas mostra PRs abertos vs fechados ao longo do tempo
- [x] Gráficos são responsivos e legíveis
- [x] Consomem dados reais de GET /metrics/weekly

## Requisito 4: Chat RAG
WHEN o usuário digitar uma pergunta no chat e enviar
THE SYSTEM SHALL enviar a query para POST /insights e exibir a resposta estruturada.

### Critérios de Aceitação
- [x] Campo de input aceita texto livre
- [x] Ao enviar, exibe estado de carregamento (loading)
- [x] Resposta exibe resumo, evidência e recomendação separadamente
- [x] Histórico de perguntas/respostas é mantido na sessão
- [x] Mensagens de erro claras quando LLM indisponível
- [x] Página dedicada para Chat RAG

## Requisito 5: Filtro de datas
WHEN o usuário selecionar um intervalo de datas
THE SYSTEM SHALL atualizar os gráficos e KPIs para refletir apenas o período selecionado.

### Critérios de Aceitação
- [x] Seletor de data com início e fim
- [x] Ao alterar, gráficos e KPIs recarregam com dados filtrados
- [x] Padrão: últimos 90 dias

## Requisito 6: Seletores de métricas
WHEN o usuário alternar quais métricas exibir
THE SYSTEM SHALL mostrar/ocultar os KPI cards e gráficos correspondentes.

### Critérios de Aceitação
- [x] Toggle para cada métrica (commits, PRs, issues)
- [x] Estado persiste durante a sessão
- [x] Pelo menos uma métrica deve estar sempre visível

## Requisito 7: Endpoint de métricas
WHEN o frontend requisitar GET /metrics
THE SYSTEM SHALL retornar KPIs calculados: commits/dia, commits/semana, PRs resolvidos, tempo médio de merge, hot repos.

### Critérios de Aceitação
- [x] Response JSON com todos os KPIs
- [x] Aceita query params opcionais: `from`, `to` (filtro de datas)
- [x] Retorna 200 com dados ou 503 se ChromaDB indisponível
- [x] Inclui tempo médio de merge (PRs)
- [x] Inclui hot repos (repositórios mais ativos)

## Requisito 8: Endpoint de métricas semanais
WHEN o frontend requisitar GET /metrics/weekly
THE SYSTEM SHALL retornar dados agregados por semana para gráficos.

### Critérios de Aceitação
- [x] Response JSON com arrays: semanas, commits por semana, PRs abertos, PRs fechados
- [x] Últimas 12 semanas
- [x] Aceita query params opcionais: `from`, `to`

## Requisito 9: Página de Configurações
WHEN o usuário acessar a página de Configurações
THE SYSTEM SHALL exibir formulário para GitHub, LLM e painel de status da ingestão.

### Critérios de Aceitação
- [x] Formulário para GITHUB_TOKEN e GITHUB_USERNAME
- [x] Seletor de provider LLM (Ollama/OpenAI)
- [x] Seletor de modelo LLM
- [x] Campo para API key OpenAI (quando selecionado)
- [x] Botão para executar ingestão manual
- [x] Painel com logs em tempo real durante ingestão
- [x] Indicadores visuais de status (Executando, Concluído, Erro)
