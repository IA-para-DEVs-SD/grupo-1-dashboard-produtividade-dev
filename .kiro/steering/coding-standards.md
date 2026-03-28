---
description: Padrões de código — tratamento de erros, commits, feedback loops, regras de qualidade
inclusion: auto
---

# Padrões de Código

## Regras gerais
- Sem imports não utilizados
- Sem código comentado em produção
- Sem números mágicos — usar constantes nomeadas
- Métodos devem fazer uma coisa e ter menos de 30 linhas quando possível
- Preferir composição sobre herança

## Tratamento de erros
- Nunca engolir exceções silenciosamente
- Usar tipos de exceção específicos, não catch-all genérico
- Logar erros com contexto (o que estava sendo feito, com qual input)
- Retornar respostas de erro significativas para os chamadores

## Feedback loops

Nunca commitar sem rodar os feedback loops.

### Loops obrigatórios (rodar após cada tarefa)
<!-- Customize para sua stack -->
```bash
# Compilação / verificação de tipos
# mvn compile | npm run typecheck | mypy src/

# Testes
# mvn test | npm test | pytest

# Linting
# mvn checkstyle:check | npm run lint | ruff check src/
```

### Regras
- NÃO commitar se qualquer feedback loop falhar. Corrija os problemas primeiro.
- Rodar loops após cada tarefa, não no final de um batch.

## Qualidade explícita

Este é código de produção. Siga os padrões existentes. Adicione testes. Trate erros. Logue de forma significativa. A IA amplifica o que vê no codebase — mantenha-o limpo.

## Commits atômicos

Uma tarefa = um commit. Formato: `type(scope): description`

Tipos: feat, fix, refactor, test, docs, chore, migration

### Regra de estado limpo
Todo commit deve deixar o codebase em estado mergeável. Sem features pela metade, sem builds quebrados.

### Proteção contra alteração de markdown
- NÃO editar tasks.md exceto para marcar checkboxes como `[x]`
- NÃO remover, reordenar ou reescrever tarefas
- Arquivos de estado (PROGRESS.md, CHANGELOG_AI.md) são append-only durante execução
