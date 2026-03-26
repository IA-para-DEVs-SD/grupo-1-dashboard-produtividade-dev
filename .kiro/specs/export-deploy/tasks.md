# Tarefas — Export e Deploy

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Criar endpoint `GET /export/csv` com StreamingResponse | R1 | 2 | ✅ Concluído |
| 2 | Criar endpoint `GET /export/pdf` com fpdf2 | R2 | 3 | ✅ Concluído |
| 3 | Criar `ExportButtons.tsx` no frontend (CSV + PDF) | R1,R2 | 1 | ✅ Concluído |
| 4 | Criar workflow `backend-ci.yml` (ruff + pytest com uv) | R3 | 2 | ✅ Concluído |
| 5 | Criar workflow `frontend-ci.yml` (build + lint com npm) | R4 | 2 | ✅ Concluído |
| 6 | Criar `vercel.json` para deploy do frontend | R5 | 2 | ✅ Concluído |
| 7 | Criar `Procfile` para deploy do backend no Railway | R6 | 3 | ✅ Concluído |
| 8 | Atualizar README com instruções de deploy e uso | — | 1 | ✅ Concluído |

## Ordem de Execução
4 → 5 → 1 → 2 → 3 → 6 → 7 → 8

## Arquivos Criados/Modificados
- `backend/src/routes/export.py` — GET /export/csv, GET /export/pdf
- `frontend/src/components/Filters/ExportButtons.tsx` — Botões de download
- `.github/workflows/backend-ci.yml` — CI do backend
- `.github/workflows/frontend-ci.yml` — CI do frontend
- `frontend/vercel.json` — Config Vercel
- `backend/Procfile` — Config Railway
- `README.md` — Documentação completa
