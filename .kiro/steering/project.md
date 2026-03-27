# Diretrizes Gerais — Dashboard de Produtividade Dev

## Visão Geral

Dashboard full-stack local-first que coleta dados do GitHub, processa com embeddings e responde perguntas via RAG. Todo processamento é local, sem serviços externos pagos.

## Arquitetura

- Monorepo com dois subprojetos Python independentes: `backend/` e `frontend/`
- Cada subprojeto tem seu próprio `pyproject.toml`, `.venv/` e `uv.lock`
- Gerenciamento exclusivo via `uv` — NUNCA usar pip, poetry ou requirements.txt

## Git e Branches

- `main` — código estável, produção. NUNCA commitar direto
- `develop` — integração contínua de features
- `feature/<nome>` — nova funcionalidade (origem: develop, destino: develop)
- `release/<versao>` — preparação de versão (destino: main + develop)
- `hotfix/<nome>` — correções urgentes (origem: main, destino: main + develop)

### Commits Semânticos (OBRIGATÓRIO)

Formato: `tipo: descrição curta`

Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Pull Requests

- Todo código entra via PR — NUNCA merge direto
- Título claro, descrição com: o que foi feito, por que, como testar
- PR deve ser revisado antes do merge

## Código Geral

- Python 3.12
- PEP 8 via Ruff: `target-version = "py312"`, `line-length = 88`, `select = ["E", "F", "W", "I"]`
- Docstrings em todas as funções e classes públicas
- Variáveis sensíveis NUNCA no código — sempre via .env
- `.gitignore` deve excluir: `.env`, `.venv/`, `__pycache__/`, `*.db`, `*.sqlite`, `chroma_data/`

## Privacidade e Segurança

- Todo processamento acontece localmente
- Tokens e credenciais ficam apenas no `.env` (nunca commitados)
- `.env.example` documenta variáveis com placeholders descritivos

## Referências

- #[[file:fluxograma_dashboard_produtividade.md]]
- #[[file:.kiro/docs-iniciais/dashboard-de-produtividade-dev.md]]
- #[[file:.kiro/docs-iniciais/gitflow_kiro_guidelines.md]]
- #[[file:.kiro/docs-iniciais/uv_kiro_guidelines.md]]
