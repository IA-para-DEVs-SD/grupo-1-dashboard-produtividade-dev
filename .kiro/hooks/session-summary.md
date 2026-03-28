---
description: Auto-atualizar STATE.md com resumo da sessão ao final do trabalho
event: manual
---

# Hook de Resumo de Sessão

## Condições
- Usuário diz "encerrar sessão", "finalizar", "terminei por hoje", ou similar
- OU o loop Ralph completa todas as tarefas de uma spec
- OU o usuário explicitamente pede para atualizar o estado

## Instruções

Ler o seguinte para entender o que aconteceu nesta sessão:
1. `git log --oneline -20` — commits recentes
2. `.kiro/state/CHANGELOG_AI.md` — o que mudou e por quê
3. Quaisquer arquivos `PROGRESS.md` em specs ativas

Então atualizar `.kiro/state/STATE.md` com um bloco de resumo de sessão:

```markdown
## YYYY-MM-DD — Resumo da sessão

### O que foi feito
- (listar tarefas concluídas, features, correções)

### O que está em progresso
- (listar trabalho parcialmente concluído, se houver)

### Próximos passos
- (listar os próximos passos lógicos)

### Riscos abertos
- (listar quaisquer novos riscos identificados durante esta sessão)
```

Regras:
- Adicionar ao STATE.md, nunca sobrescrever entradas anteriores
- Ser específico — referenciar nomes de specs, números de tarefas, nomes de arquivos
- Se uma spec foi concluída, notar e mencionar se foi arquivada
- Se decisões foram tomadas, verificar se também estão em DECISIONS.md
