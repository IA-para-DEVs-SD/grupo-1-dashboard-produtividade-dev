# Rubrica de Qualidade — Dashboard Produtividade Dev

**Total: 100 pontos**

---

## 1. Qualidade de Código (30 pts)

| Critério | Pontos | O que avaliar |
|----------|--------|---------------|
| **1.1 Linting e formatação** | 5 | `ruff check` passa sem erros em `backend/` e `frontend/`. Configuração consistente no `pyproject.toml` (line-length, target-version, select rules). |
| **1.2 Organização e separação de responsabilidades** | 6 | Camadas bem definidas: routes → services → models. Sem lógica de negócio em rotas. Sem imports circulares. Cada módulo tem responsabilidade única. |
| **1.3 Tipagem e contratos** | 5 | Type hints em funções públicas. Pydantic/SQLModel para validação de dados. Retornos tipados nas rotas FastAPI. |
| **1.4 Tratamento de erros** | 5 | Try/except com logging adequado (loguru + correlation ID). Erros não silenciados. Respostas HTTP com status codes corretos. Fallbacks no pipeline RAG. |
| **1.5 Testes** | 5 | Cobertura dos módulos principais (collector, pipeline, config, models, ingestion, metrics). Testes de propriedade com Hypothesis onde aplicável. CI executa testes automaticamente. |
| **1.6 Ausência de code smells** | 4 | Sem código duplicado. Sem funções > 50 linhas. Sem hardcoded values que deveriam ser config. Sem TODO/FIXME abandonados. Sem imports não utilizados. |

### Como pontuar

| Faixa | Descrição |
|-------|-----------|
| 27–30 | Código limpo, bem tipado, testado, sem warnings de lint |
| 20–26 | Boa estrutura com pequenas falhas (tipagem incompleta, poucos testes faltando) |
| 12–19 | Estrutura razoável mas com problemas visíveis (erros silenciados, camadas misturadas) |
| 0–11 | Código desorganizado, sem testes, lint falhando |

---

## 2. Clareza da Documentação (20 pts)

| Critério | Pontos | O que avaliar |
|----------|--------|---------------|
| **2.1 README.md** | 6 | Contém: descrição do projeto, tecnologias, arquitetura (diagrama), instruções de instalação, variáveis de ambiente, como executar. |
| **2.2 Docstrings** | 4 | Funções e classes públicas documentadas. Docstrings descrevem propósito, parâmetros e retorno. |
| **2.3 .env.example** | 3 | Todas as variáveis obrigatórias presentes. Placeholders descritivos (não vazios). Comentários explicando variáveis não óbvias. |
| **2.4 Specs e decisões técnicas** | 4 | Specs em `.kiro/specs/` documentam requisitos, design e tarefas. Decisões de arquitetura registradas (ex: por que ChromaDB, por que aisuite). |
| **2.5 Consistência** | 3 | Informações no README batem com o código real (portas, modelos, comandos). Sem referências a tecnologias não utilizadas. Sem seções placeholder vazias. |

### Como pontuar

| Faixa | Descrição |
|-------|-----------|
| 18–20 | Documentação completa, consistente, um dev novo consegue rodar o projeto só lendo |
| 13–17 | Boa documentação com pequenas inconsistências ou seções faltando |
| 7–12 | Documentação parcial, faltam instruções importantes |
| 0–6 | README mínimo ou ausente, sem docstrings |

---

## 3. Segurança (20 pts)

| Critério | Pontos | O que avaliar |
|----------|--------|---------------|
| **3.1 Gestão de secrets** | 5 | Tokens e API keys via `.env` (nunca hardcoded). `.gitignore` exclui `.env`, `*.db`, `chroma_data/`. `.env.example` usa placeholders, não valores reais. |
| **3.2 CORS e rate limiting** | 4 | CORS configurado com origens explícitas (não `*` em produção). Rate limiting ativo via slowapi. |
| **3.3 Validação de entrada** | 4 | Inputs validados via Pydantic models nas rotas. Query parameters sanitizados. Sem SQL injection (uso de ORM). |
| **3.4 Dependências** | 4 | Versões fixadas no `pyproject.toml`. Sem dependências com vulnerabilidades conhecidas. Lock files commitados (`uv.lock`). |
| **3.5 Exposição de dados** | 3 | Health check detalhado não vaza informações sensíveis. Erros retornados ao cliente não expõem stack traces. Logs não registram tokens ou dados pessoais. |

### Como pontuar

| Faixa | Descrição |
|-------|-----------|
| 18–20 | Secrets protegidos, CORS restrito, inputs validados, deps atualizadas |
| 13–17 | Boas práticas com pequenas falhas (CORS permissivo demais, uma validação faltando) |
| 7–12 | Problemas visíveis (secrets no código, sem rate limiting, CORS aberto) |
| 0–6 | Falhas graves de segurança |

---

## 4. Maturidade de Engenharia do Time (30 pts)

> Critério próprio: avalia práticas de engenharia que vão além do código — o quanto o time opera como uma equipe profissional de software.

| Critério | Pontos | O que avaliar |
|----------|--------|---------------|
| **4.1 CI/CD funcional** | 7 | GitHub Actions configurado para backend e frontend. Pipeline roda lint + testes em push/PR. Builds reproduzíveis com `uv sync`. |
| **4.2 Containerização** | 5 | Dockerfiles para backend e frontend. `docker-compose.yml` sobe o stack completo (Ollama + backend + frontend). Volumes persistentes configurados. |
| **4.3 GitFlow e commits semânticos** | 6 | Branches `main`/`develop`/`feature/*` usadas corretamente. Commits seguem formato semântico (`feat:`, `fix:`, `docs:`, etc.). PRs com descrição clara. |
| **4.4 Observabilidade** | 5 | Logging estruturado com loguru + correlation IDs. Health checks (básico + detalhado). Endpoints de status para serviços externos (GitHub, LLM, ChromaDB). |
| **4.5 Reprodutibilidade do ambiente** | 4 | `.python-version` definido. `uv.lock` commitado. `.env.example` completo. Qualquer dev consegue rodar `uv sync && uv run` e funciona. |
| **4.6 Specs e planejamento** | 3 | Features planejadas via specs antes de implementar. Requisitos, design e tasks documentados. Rastreabilidade entre spec e código. |

### Como pontuar

| Faixa | Descrição |
|-------|-----------|
| 27–30 | CI/CD rodando, Docker funcional, GitFlow seguido, observabilidade completa |
| 20–26 | Boa infraestrutura com gaps menores (CI sem coverage, commits inconsistentes) |
| 12–19 | Infraestrutura parcial (CI básico, sem Docker ou sem GitFlow) |
| 0–11 | Sem CI, sem containers, sem padrão de branches ou commits |

---

## Resumo da Pontuação

| Critério | Peso | Nota | Subtotal |
|----------|------|------|----------|
| 1. Qualidade de Código | 30 | ___ / 30 | |
| 2. Clareza da Documentação | 20 | ___ / 20 | |
| 3. Segurança | 20 | ___ / 20 | |
| 4. Maturidade de Engenharia do Time | 30 | ___ / 30 | |
| **TOTAL** | **100** | | **___ / 100** |

### Classificação Final

| Faixa | Classificação |
|-------|---------------|
| 90–100 | Excelente — projeto pronto para produção |
| 75–89 | Bom — sólido com melhorias pontuais |
| 55–74 | Regular — funcional mas precisa de atenção |
| 0–54 | Insuficiente — requer refatoração significativa |
