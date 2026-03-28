# 🏃 Sprint 2 — Ingestão de Dados do GitHub

> Objetivo: Conectar à GitHub GraphQL API e coletar commits, PRs e issues dos últimos 90 dias, parseando em chunks de texto.

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar classe `GitHubCollector` com autenticação via token | R06 | 3 | 🔲 A fazer |
| 2 | Implementar `fetch_commits()` via GraphQL — últimos 90 dias | R07 | 3 | 🔲 A fazer |
| 3 | Implementar `fetch_pull_requests()` via GraphQL | R08 | 3 | 🔲 A fazer |
| 4 | Implementar `fetch_issues()` via GraphQL | R09 | 2 | 🔲 A fazer |
| 5 | Criar modelo `Commit` com `sha, message, author, date, additions, deletions` | R07 | 1 | 🔲 A fazer |
| 6 | Criar modelos `PullRequest` e `Issue` com campos relevantes | R08,R09 | 1 | 🔲 A fazer |
| 7 | Implementar `to_chunk()` em cada modelo — converte para texto embedável | R10 | 2 | 🔲 A fazer |
| 8 | Criar parser que recebe JSON raw → lista de chunks de texto | R10 | 2 | 🔲 A fazer |
| 9 | Endpoint `GET /github/status` — verifica conexão com token | R06 | 1 | 🔲 A fazer |
| 10 | Testes unitários para parser e modelos (mock de resposta GraphQL) | R07-R10 | 2 | 🔲 A fazer |

## Critérios de Conclusão
- `GitHubCollector` busca commits, PRs e issues reais via GraphQL
- Cada entidade tem método `to_chunk()` que gera texto legível
- Parser converte JSON → lista de strings prontas para embedding
- Testes passam com dados mockados
