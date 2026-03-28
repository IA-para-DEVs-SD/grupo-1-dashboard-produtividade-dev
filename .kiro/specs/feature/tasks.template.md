# 📋 Tarefas — [Nome da Feature]

## Painel de Progresso

| Métrica | Valor |
|---------|-------|
| Total de Tarefas | <!-- N --> |
| Concluídas | <!-- 0/N --> |
| Verificação | <!-- ✅ Todas passaram / ⚠️ Pendente / ❌ Tem falhas --> |
| Nível de Risco | <!-- 🟢 Baixo / 🟡 Médio / 🔴 Alto --> |
| Modo de Execução | <!-- HITL / AFK --> |

## Feedback Loops

Rodar após cada tarefa. NÃO commitar se algum falhar.

```bash
# Substitua pelos comandos reais do seu projeto
mvn test                    # testes devem passar
mvn compile                 # tipos/compilação devem passar
mvn checkstyle:check        # lint deve passar
```

## Lista de Tarefas

<!-- Legenda de status:
  [✅] — Concluída + verificada (Truth Loop passou)
  [⚠️] — Concluída, verificação pendente
  [❌] — Verificação falhou
  [🔄] — Em progresso
  [ ]  — Não iniciada
-->

### [ ] Tarefa 1: [Título]
- **Risco:** <!-- 1-5 (1=baixo, 5=alto) → motivo -->
- **Descrição:** <!-- O que fazer — uma coisa apenas -->
- **Arquivos:** <!-- Arquivos esperados para criar/modificar -->
- **Critérios de conclusão:**
  - [ ] <!-- ex: Teste unitário passa -->
  - [ ] <!-- ex: Migração roda sem erro -->
  - [ ] Feedback loops passam
- **Commit:** `<!-- ex: feat(auth): add login endpoint -->`
- **Dependências:** <!-- Outras tarefas que devem ser feitas primeiro, ou "nenhuma" -->

### [ ] Tarefa 2: [Título]
- **Risco:** <!-- 1-5 → motivo -->
- **Descrição:**
- **Arquivos:**
- **Critérios de conclusão:**
  - [ ]
  - [ ] Feedback loops passam
- **Commit:** `<!-- -->`
- **Dependências:**

<!-- Adicione mais tarefas conforme necessário -->

## Ordem de Execução

Tarefas ordenadas por risco (maior primeiro):

1. Tarefa 1 — <!-- por que primeiro: decisão arquitetural / ponto de integração / spike -->
2. Tarefa 2 — <!-- motivo -->

## Resumo de Verificação

<!-- Preenchido pelo Truth Loop após verificação -->

| Tarefa | Status | Notas |
|--------|--------|-------|
| Tarefa 1 | <!-- ✅ / ⚠️ / ❌ --> | <!-- --> |
| Tarefa 2 | <!-- ✅ / ⚠️ / ❌ --> | <!-- --> |

## Notas

- Cada tarefa = uma iteração Ralph = um commit atômico
- Se uma tarefa toca > 5 arquivos, dividir
- Nunca ultrapassar seus feedback loops
