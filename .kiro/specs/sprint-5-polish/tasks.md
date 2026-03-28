# 🏃 Sprint 5 — Polimento, CI/CD e Deploy

> Objetivo: Export de relatórios, pipeline CI/CD, deploy em produção (Vercel + Railway).

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Export CSV: endpoint `GET /export/csv` + botão no frontend | R26 | 2 | 🔲 A fazer |
| 2 | Export PDF: gerar relatório com insights + gráficos | R26 | 3 | 🔲 A fazer |
| 3 | Workflow GitHub Actions: lint (ruff) + test (pytest) no backend | R27 | 2 | 🔲 A fazer |
| 4 | Workflow GitHub Actions: build + lint no frontend | R27 | 2 | 🔲 A fazer |
| 5 | Configurar deploy do frontend no Vercel (vercel.json + variáveis de ambiente) | R28 | 2 | 🔲 A fazer |
| 6 | Configurar deploy do backend no Railway (Procfile + variáveis de ambiente) | R29 | 3 | 🔲 A fazer |
| 7 | Documentação OpenAPI/Swagger (automática do FastAPI) — revisar e completar | R30 | 1 | 🔲 A fazer |
| 8 | README final com instruções de setup, deploy e uso | R30 | 1 | 🔲 A fazer |

## Critérios de Conclusão
- Export CSV e PDF funcionais
- CI/CD roda em cada push (lint + test + build)
- Frontend no ar no Vercel
- Backend no ar no Railway
- Swagger UI acessível em `/docs`
- README completo e atualizado
