# Prompts utilizados no projeto

Registro dos prompts usados durante o desenvolvimento do projeto com auxílio de IA.

---

## 1. Atualizar projeto com repositório remoto

```
atualize o projeto de acordo com o repositório remoto
```

Resultado: sincronização da branch local com `origin`, trazendo novas branches remotas (`feat/criar-readme`, `feature/fluxograma`, `feature/specs-edemilson`) e atualizações em `main` e `develop`.

---

## 2. Refatorar projeto conforme diretrizes

```
refatore o projeto de acordo com as diretrizes:

Estrutura padrão de repositórios

Padrão de nomenclatura dos repositórios de projetos
Nome grupo + Nome do projeto: Exemplo: "grupo-x-nome-projeto"
Não utilizar caracteres especiais além do hífen
Texto sempre em minúsculo

Padrão de nomenclatura dos repositórios de atividades
Nome grupo + Atividades + Nome aluno: Exemplo: "grupo-x-atividades-fulano-sobrenome"
Não utilizar caracteres especiais além do hífen
Texto sempre em minúsculo

Padrão do Gitflow
Branch principal: main
Branch desenvolvimento: develop
Branch de novas funcionalidades: feature/issue-xxx

Padrão do commit semântico
"tipo: breve descrição
descrição mais detalhada (opcional)"
Tipos:
feat: Nova funcionalidade
docs: Documentações
fix: Correções
refactor: Refatorações
tests: Testes unitários, etc

Padrão de nomenclatura dos boards / projetos
Identificação do Grupo + Nome do Projeto
Exemplo: "Grupo X - Nome Projeto"

Padrão de tópicos do README
Nome do Projeto
Breve descrição do projeto
Sumário de documentações
Tecnologias utilizadas
Instruções de instalação / uso
Integrantes do grupo
```

Resultado: `main` atualizada, branch `develop` criada localmente, branch `feature/issue-001` criada a partir de `develop`, README refatorado com todos os tópicos obrigatórios e commit semântico aplicado.

---

## 3. Abrir Pull Request

```
Pode seguir com o PR
```

Resultado: push da branch `feature/issue-001` para o remoto e tentativa de abertura do PR via `gh` CLI. Como o CLI não estava instalado, o PR foi aberto manualmente pelo link gerado pelo GitHub.

---

## 4. Registrar prompts do projeto

```
Olá, crie uma pasta docs no diretório e um arquivo em .md e registre todos os prompts que usamos até agora para gerar o projeto
```

Resultado: criação deste arquivo em `docs/prompts.md`.

---

## 5. Criação e correção de testes unitários e de integração

```
atue como um dev senior especialista em python e testes
vamos corrigir os testes unitários que estão quebrados
criar novos testes para o front e backend
criar testes de integração, no mínimo 5 testes de integração
os testes de fato tem que validar as regras do sistema, não ser somente testes genéricos
após a conclusão, adicione nosso prompt como documentação no arquivo loading dentro de docs
```

Resultado: branch `feature/criacao_testes` criada a partir de `develop`.

**Correções realizadas:**
- `backend/tests/conftest.py` — criado para mockar `sentence-transformers` e `openai` no nível de `sys.modules`, evitando erros de import em ambientes sem essas dependências pesadas. Reseta singletons entre testes.
- `backend/tests/test_main.py` — corrigido para mockar `start_scheduler` e `_get_model` antes de importar o app FastAPI.
- `backend/tests/test_pipeline.py` — reescrito para usar fixture simples com `RAGPipeline.__new__` e mocks diretos.

**Novos testes unitários — Backend:**

| Arquivo | Módulo testado | Regras validadas |
|---------|---------------|------------------|
| `test_config.py` | `src/config.py` | Defaults do Settings (ollama, llama3.1, 90 dias, CORS 8501) |
| `test_collector.py` | `src/github/collector.py` | Auth com bearer token, check_connection, parsing GraphQL, resiliência a falhas parciais |
| `test_ingestion.py` | `src/services/ingestion.py` | Status tracking, retorno 0 sem token, fluxo completo de ingestão, scheduler 12h |
| `test_metrics_service.py` | `src/services/metrics.py` | KPIs (commits, PRs merged, hot repos, tempo merge), cache em memória, erro sem token |
| `test_settings_routes.py` | `src/routes/settings.py` | Validação formato token GitHub (ghp_/ghs_/github_pat_), rejeição de tokens inválidos, config LLM |

**Novos testes unitários — Frontend:**

| Arquivo | Módulo testado | Regras validadas |
|---------|---------------|------------------|
| `test_api_client.py` | `src/api_client.py` | URLs de export com/sem datas, endpoints GitHub/métricas/insights/LLM/ingestão, passagem de parâmetros |

**Testes de integração — Backend:**

| # | Classe | Fluxo testado |
|---|--------|---------------|
| 1 | `TestInsightsValidation` | POST /insights com query vazia → 400, sem campo query → 422 |
| 2 | `TestInsightsPipelineIntegration` | POST /insights → RAGPipeline → Insight com todos os campos |
| 3 | `TestExportCSVIntegration` | GET /export/csv → MetricsService → CSV com headers e dados |
| 4 | `TestIngestTriggerIntegration` | POST /ingest → background task, GET /ingest/status → campos de monitoramento |
| 5 | `TestMetricsEndpointIntegration` | GET /metrics → GitHubCollector (mock) → KPIs calculados |
| 6 | `TestHealthDetailedIntegration` | GET /health/detailed → checks de api/chromadb/github/llm, status degraded vs ok |

**Resultado final:** Backend: 77 testes passando. Frontend: 11 testes passando. Total: 88 testes.
