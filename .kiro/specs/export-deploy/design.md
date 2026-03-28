# Design — Export e Deploy

## Visão Geral
Funcionalidades de exportação de dados (CSV/PDF) e configuração de CI/CD + deploy em produção.

## Componentes

### Rotas de Export (`backend/src/routes/export.py`)
- `GET /export/csv?from=&to=` — gera CSV com métricas do período
- `GET /export/pdf?from=&to=` — gera PDF com relatório resumido
- Usa `StreamingResponse` do FastAPI para download direto

### Geração de CSV
- Usa módulo `csv` nativo do Python
- Dados vêm do serviço de métricas (mesmo que `GET /metrics`)

### Geração de PDF
- Usa `reportlab` ou `fpdf2` para gerar PDF simples
- Inclui: título, período, tabela de KPIs, resumo textual

### Botões de Export (`frontend/src/components/Filters/`)
- `ExportButtons.tsx` — botões CSV e PDF que disparam download via `window.open(url)`

### CI/CD (`.github/workflows/`)
- `backend-ci.yml` — lint + test no backend com `uv`
- `frontend-ci.yml` — build + lint no frontend com npm
- Trigger: push em `develop` e `main`

### Deploy
- **Vercel**: configuração via `vercel.json` + variáveis de ambiente no painel
- **Railway**: configuração via `Procfile` (`web: uvicorn src.main:app --host 0.0.0.0 --port $PORT`)

## Decisões Técnicas
- **CSV nativo**: sem dependência extra, `csv.writer` é suficiente
- **fpdf2 para PDF**: leve, sem dependências de sistema (diferente de wkhtmltopdf)
- **CI separado por camada**: backend e frontend rodam em paralelo no GitHub Actions
- **Deploy automático**: sem step manual, merge em main = produção

## Dependências
- `fpdf2` — geração de PDF (backend)
