---
description: Padrões e convenções específicas do Python FastAPI
inclusion: auto
---

# FastAPI Overlay

## Stack
- Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x async, Alembic
- uvicorn para ASGI, httpx para cliente HTTP, structlog para logging

## Convenções
- Type hints em todas as assinaturas de função — sem `Any` a menos que realmente necessário
- `str | None` e não `Optional[str]` (sintaxe Python 3.10+)
- `async def` para handlers I/O-bound, `def` para CPU-bound
- `Depends()` para injeção de dependência — nunca instanciar serviços dentro dos handlers
- Schemas Pydantic separados para request e response: `CreateUserRequest`, `UserResponse`
- `pydantic-settings` para configuração tipada de ambiente

## Testes
- `pytest` + `pytest-asyncio` + `httpx.AsyncClient` para testes de API
- Testcontainers para testes de banco (mesma versão PostgreSQL da produção)
- Migrações Alembic rodam no setup dos testes

## Feedback loops
```bash
mypy src/
pytest
ruff check src/
ruff format --check src/
```

## Segurança
- `Depends()` para injeção de auth — nunca verificar auth dentro do corpo do handler
- CORS: configurar em `main.py`, nunca `allow_origins=["*"]` em produção
- Desabilitar `/docs` e `/redoc` em produção ou proteger com autenticação
