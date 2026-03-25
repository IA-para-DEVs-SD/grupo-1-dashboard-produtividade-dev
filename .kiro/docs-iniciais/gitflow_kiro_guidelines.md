# Regras Obrigatórias: Git + GitFlow (Kiro Steering)

## Diretriz Principal

Use Git seguindo o padrão **GitFlow** para garantir organização, rastreabilidade e segurança no desenvolvimento.

NUNCA trabalhe diretamente na `main` sem controle.

---

## 1. Estrutura de Branches

### Branches principais

- `main`
  
  - Contém código **estável e em produção**
  - Nunca deve quebrar

- `develop`
  
  - Integração contínua de features
  - Base para novas funcionalidades

---

### Branches auxiliares

- `feature/<nome>`
  
  - Nova funcionalidade
  - Origem: `develop`
  - Destino: `develop`

- `release/<versao>`
  
  - Preparação de versão
  - Origem: `develop`
  - Destino: `main` e `develop`

- `hotfix/<nome>`
  
  - Correções urgentes
  - Origem: `main`
  - Destino: `main` e `develop`

---

## 2. Regras de Commit

### Quando fazer commit

Faça commit quando:

- Uma unidade lógica de trabalho estiver concluída
- Um bug foi corrigido
- Um comportamento foi alterado de forma clara
- Antes de mudar de contexto/tarefa
- Antes de abrir um Pull Request

NÃO faça commit:

- com código quebrado
- com arquivos irrelevantes
- com mensagens genéricas

---

## 3. Commits Semânticos (OBRIGATÓRIO)

Formato:

```
tipo: descrição curta
```

Tipos permitidos:

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `refactor`: melhoria sem alteração de comportamento
- `test`: testes
- `chore`: tarefas internas

Exemplos:

```bash
feat: adiciona autenticação JWT
fix: corrige erro de validação no login
docs: atualiza README com instruções
refactor: simplifica lógica de cálculo
```

---

## 4. Pull Requests (PR)

### Obrigatório

- Todo código deve entrar via PR
- Nunca fazer merge direto na `main`
- PR deve ser revisado antes do merge

### Padrão de PR

- Título claro
- Descrição objetiva:
  - O que foi feito
  - Por que foi feito
  - Como testar
- Incluir prints (se aplicável)

---

## 5. Code Review

- Revisar linha por linha
- Sugerir melhorias
- Verificar:
  - legibilidade
  - performance
  - boas práticas
  - segurança

---

## 6. Fluxo de Trabalho

### Nova funcionalidade

```bash
git checkout develop
git pull
git checkout -b feature/nova-feature
```

Trabalhar → commits → push

```bash
git push origin feature/nova-feature
```

Abrir PR → merge em `develop`

---

### Release

```bash
git checkout -b release/1.0.0 develop
```

Ajustes finais → merge em `main` e `develop`

---

### Hotfix

```bash
git checkout -b hotfix/correcao main
```

Corrigir → merge em `main` e `develop`

---

## 7. Regras Críticas

PROIBIDO:

- Commit direto na `main`
- Merge sem PR
- Commit sem mensagem semântica
- Branches longas e desatualizadas

OBRIGATÓRIO:

- Usar branches
- Usar PR
- Fazer code review
- Manter histórico limpo

---

## 8. Regra de Ouro

Se não passou por:

- branch
- commit semântico
- pull request
- review

Então NÃO deve ir para produção.
