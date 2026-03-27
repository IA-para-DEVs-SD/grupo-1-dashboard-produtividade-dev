---
inclusion: fileMatch
fileMatchPattern: "frontend/**"
---

# Diretrizes — Frontend

## Stack

- Framework: Streamlit
- Gráficos: Plotly
- Comunicação com backend via `requests` usando `BACKEND_API_URL` do .env
- Porta configurável via `STREAMLIT_SERVER_PORT` no .env (default 8501)

## Estrutura de Pastas

```
frontend/
├── src/
│   ├── __init__.py
│   └── app.py            # App Streamlit principal
├── tests/
├── docs/
├── pyproject.toml
└── .python-version       # 3.12
```

## Gerenciamento de Dependências

- SEMPRE usar `uv add` para adicionar dependências
- SEMPRE usar `uv add --dev` para dependências de desenvolvimento
- SEMPRE usar `uv run` para executar código
- SEMPRE commitar `uv.lock`
- NUNCA usar `pip`, `poetry` ou `requirements.txt`

## Execução

```bash
cd frontend
cp .env.example .env
uv sync
uv run streamlit run src/app.py
```

O frontend estará disponível em `http://localhost:8501`.

## Variáveis de Ambiente (`frontend/.env`)

```env
BACKEND_API_URL=http://localhost:8000
STREAMLIT_SERVER_PORT=8501
```

## Testes

- Testes unitários com pytest para toda funcionalidade nova
- Executar: `uv run pytest`
