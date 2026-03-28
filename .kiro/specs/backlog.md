# 📋 Backlog do Produto

> Última atualização: 2026-03-25

## Specs por Feature

| Spec | Diretório | Requisitos | Tarefas |
|------|-----------|------------|---------|
| Ingestão GitHub | `specs/github-ingestion/` | 6 (EARS) | 8 |
| Pipeline RAG | `specs/rag-pipeline/` | 7 (EARS) | 10 |
| Dashboard Frontend | `specs/dashboard-frontend/` | 7 (EARS) | 10 |
| Export e Deploy | `specs/export-deploy/` | 6 (EARS) | 8 |

## Ordem de Execução das Features

| # | Feature | Depende de | Status |
|---|---------|------------|--------|
| 0 | Setup do projeto (backend + frontend) | — | 🔲 A fazer |
| 1 | Ingestão GitHub | Setup | 🔲 A fazer |
| 2 | Pipeline RAG | Ingestão GitHub | 🔲 A fazer |
| 3 | Dashboard Frontend | Pipeline RAG (backend) | 🔲 A fazer |
| 4 | Export e Deploy | Todas as anteriores | 🔲 A fazer |

## Notas

- O setup do projeto (Sprint 1 do KiroRails) não tem spec própria — são tarefas de infraestrutura gerenciadas via `kirorails sprint`
- Cada spec contém `requirements.md` (EARS), `design.md` e `tasks.md`
- O PRD macro do produto está em `steering/product.md`
- A stack técnica está em `steering/tech.md`
- A estrutura do projeto está em `steering/structure.md`

## Legenda de Status

- 🔲 A fazer — não iniciado
- 🔄 Em progresso — em desenvolvimento
- ✅ Concluído — implementado e verificado
- ❌ Bloqueado — tem impedimentos
