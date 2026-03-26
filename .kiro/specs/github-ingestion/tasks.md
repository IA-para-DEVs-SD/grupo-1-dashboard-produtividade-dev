# Tarefas — Ingestão de Dados do GitHub

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar modelos Pydantic: `Commit`, `PullRequest`, `Issue` com `to_chunk()` e `to_metadata()` | R4 | 1 | ✅ Concluído |
| 2 | Criar `GitHubCollector` com autenticação via token e config | R1 | 2 | ✅ Concluído |
| 3 | Implementar `fetch_commits()` com query GraphQL + paginação cursor (5 páginas) | R1 | 3 | ✅ Concluído |
| 4 | Implementar `fetch_pull_requests()` com query GraphQL + paginação cursor | R2 | 3 | ✅ Concluído |
| 5 | Implementar `fetch_issues()` com query GraphQL + paginação cursor | R3 | 2 | ✅ Concluído |
| 6 | Implementar tratamento de erros: retry, rate limit, logging | R6 | 3 | ✅ Concluído |
| 7 | Criar rota `GET /github/status` | R5 | 1 | ✅ Concluído |
| 8 | Criar rota `GET /settings/github` e `POST /settings/github` | R7 | 2 | ✅ Concluído |
| 9 | Criar página de Configurações no frontend com formulário GitHub | R7 | 2 | ✅ Concluído |
| 10 | Validação de formato do token GitHub (regex) | R7 | 1 | ✅ Concluído |
| 11 | Persistir configurações em arquivo .env | R7 | 2 | ✅ Concluído |
| 12 | Criar testes unitários para models (to_chunk, to_metadata) | R8 | 2 | ✅ Concluído |

## Arquivos Criados/Modificados
- `backend/src/github/models.py` — Modelos Commit, PullRequest, Issue
- `backend/src/github/collector.py` — GitHubCollector com GraphQL
- `backend/src/routes/github.py` — GET /github/status
- `backend/src/routes/settings.py` — GET/POST /settings/github com validação e persistência
- `backend/tests/test_models.py` — Testes unitários para models
- `frontend/src/pages/SettingsPage.tsx` — Página de configurações
