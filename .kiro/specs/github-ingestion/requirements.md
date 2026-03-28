# Requisitos — Ingestão de Dados do GitHub

## Requisito 1: Coleta de commits
WHEN o cron de ingestão for executado
THE SYSTEM SHALL buscar todos os commits do usuário nos últimos 90 dias via GitHub GraphQL API.

### Critérios de Aceitação
- [x] Dado que o token GitHub esteja configurado e válido
- [x] Quando o cron executar
- [x] Então o sistema deve retornar commits com: sha, mensagem, autor, data, adições e deleções
- [x] E implementar paginação com cursor para volumes > 100 commits
- [x] E buscar até 500 commits por repositório (5 páginas × 100)

## Requisito 2: Coleta de Pull Requests
WHEN o cron de ingestão for executado
THE SYSTEM SHALL buscar todos os PRs (abertos e fechados) do usuário nos últimos 90 dias.

### Critérios de Aceitação
- [x] Dado que o token tenha escopo `repo`
- [x] Quando o cron executar
- [x] Então o sistema deve retornar PRs com: título, estado, data de criação, data de merge, repositório
- [x] E incluir tanto PRs abertos quanto fechados/merged
- [x] E implementar paginação com cursor (5 páginas × 100)

## Requisito 3: Coleta de Issues
WHEN o cron de ingestão for executado
THE SYSTEM SHALL buscar todas as issues criadas ou resolvidas pelo usuário nos últimos 90 dias.

### Critérios de Aceitação
- [x] Quando o cron executar
- [x] Então o sistema deve retornar issues com: título, estado, labels, data de criação, data de fechamento
- [x] E implementar paginação com cursor (5 páginas × 100)

## Requisito 4: Conversão para chunks de texto
WHEN os dados brutos do GitHub forem coletados
THE SYSTEM SHALL converter cada entidade (commit, PR, issue) em um chunk de texto legível para embedding.

### Critérios de Aceitação
- [x] Dado um commit com sha, mensagem e metadados
- [x] Quando `to_chunk()` for chamado
- [x] Então deve retornar uma string como: "Commit abc123: feat: auth JWT — 50 adições, 10 deleções — autor: sergio — 2026-03-20"
- [x] E cada chunk deve conter metadados suficientes para contexto no RAG
- [x] E `to_metadata()` deve retornar dict com tipo, data, repositório, autor

## Requisito 5: Verificação de conexão
WHEN o usuário acessar GET /github/status
THE SYSTEM SHALL verificar se o token GitHub está válido e retornar o status da conexão.

### Critérios de Aceitação
- [x] Dado um token válido, retorna `{"connected": true, "username": "..."}`
- [x] Dado um token inválido ou ausente, retorna `{"connected": false, "error": "..."}`

## Requisito 6: Resiliência a falhas da API
WHEN a GitHub API retornar erro ou timeout
THE SYSTEM SHALL registrar o erro no log e não interromper o funcionamento da aplicação.

### Critérios de Aceitação
- [x] Dado que a API retorne 403 (rate limit) ou 500
- [x] Quando o coletor tentar buscar dados
- [x] Então deve logar o erro com loguru
- [x] E não lançar exceção não tratada
- [x] E manter os dados da última ingestão bem-sucedida

## Requisito 7: Configuração via interface
WHEN o usuário acessar a página de Configurações
THE SYSTEM SHALL permitir configurar GITHUB_TOKEN e GITHUB_USERNAME via formulário.

### Critérios de Aceitação
- [x] Formulário com campos para username e token
- [x] Botão salvar que persiste em .env no backend
- [x] Indicador visual de status (conectado/desconectado)
- [x] Validação de formato do token (regex ghp_/ghs_)

## Requisito 8: Testes unitários
WHEN o código for modificado
THE SYSTEM SHALL ter testes cobrindo models e pipeline.

### Critérios de Aceitação
- [x] Testes para Commit, PullRequest, Issue (to_chunk, to_metadata)
- [x] Testes para RAGPipeline (build_prompt, query scenarios)
- [x] Todos os testes passando com pytest
