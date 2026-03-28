# Design — Ingestão de Dados do GitHub

## Visão Geral
Módulo responsável por conectar à GitHub GraphQL API, coletar dados de atividade do desenvolvedor e transformá-los em chunks de texto prontos para embedding.

## Componentes

### GitHubCollector (`backend/src/github/collector.py`)
- Recebe `token` e `days_back` (padrão: 90) via config
- Usa `httpx` (async) para chamadas GraphQL
- Métodos: `fetch_commits()`, `fetch_pull_requests()`, `fetch_issues()`
- Trata paginação com cursors do GraphQL
- Retry com backoff exponencial em caso de rate limit (403)

### Modelos de Domínio (`backend/src/github/models.py`)
- `Commit`: sha, message, author, date, additions, deletions
- `PullRequest`: title, state, created_at, merged_at, repository
- `Issue`: title, state, labels, created_at, closed_at
- Cada modelo implementa `to_chunk() -> str`

### Rota de Status (`backend/src/routes/github.py`)
- `GET /github/status` — chama GraphQL `viewer { login }` para validar token

## Queries GraphQL

```graphql
# Commits — via contributionsCollection
query($from: DateTime!, $to: DateTime!) {
  viewer {
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository {
        repository { nameWithOwner }
        contributions(first: 100) {
          nodes { occurredAt commitCount }
        }
      }
    }
  }
}
```

## Decisões Técnicas
- **GraphQL em vez de REST**: menos requests, dados mais ricos em uma chamada
- **httpx async**: não bloqueia o event loop do FastAPI
- **Pydantic models**: validação automática dos dados da API
- **Chunks com metadados inline**: facilita o RAG entender contexto sem depender de metadata separada

## Dependências
- `httpx` — cliente HTTP async
- `pydantic` — modelos de dados (já incluso no FastAPI)
