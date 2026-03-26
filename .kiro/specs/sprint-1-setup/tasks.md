# 🏃 Sprint 1 — Setup e Fundação do Projeto

> Objetivo: Scaffold do backend (FastAPI + uv) e frontend (React + Vite), configurar env, health check e logging.

## Tarefas

| # | Tarefa | Reqs | Risco | Status |
|---|--------|------|-------|--------|
| 1 | Iniciar backend: `uv init`, `pyproject.toml` com FastAPI, uvicorn, loguru, ruff, pytest | R01 | 1 | 🔲 A fazer |
| 2 | Criar `backend/src/main.py` com app FastAPI + middleware CORS | R01 | 1 | 🔲 A fazer |
| 3 | Criar endpoint `GET /health` retornando `{"status": "ok"}` | R04 | 1 | 🔲 A fazer |
| 4 | Setup de logging com loguru + middleware de correlation ID | R05 | 2 | 🔲 A fazer |
| 5 | Criar `backend/.env.example` com todas as variáveis documentadas | R03 | 1 | 🔲 A fazer |
| 6 | Config loader: Pydantic Settings para carregar .env | R03 | 2 | 🔲 A fazer |
| 7 | Iniciar frontend: Vite + React 18 + TypeScript scaffold | R02 | 1 | 🔲 A fazer |
| 8 | Instalar Chart.js + react-chartjs-2 no frontend | R02 | 1 | 🔲 A fazer |
| 9 | Criar `frontend/.env.example` com `VITE_API_URL` | R03 | 1 | 🔲 A fazer |
| 10 | Verificar: `uv run uvicorn src.main:app` sobe sem erro | R01,R04 | 1 | 🔲 A fazer |

## Critérios de Conclusão
- Backend sobe com `uv run uvicorn src.main:app --reload`
- `GET /health` retorna 200
- Frontend sobe com `npm run dev`
- Logging funcional com correlation ID
- `.env.example` documentado em ambos
