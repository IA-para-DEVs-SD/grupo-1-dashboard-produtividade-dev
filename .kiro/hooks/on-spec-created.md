---
description: Validar completude da spec quando uma nova spec é criada ou modificada
event: on_file_save
---

## Condições

- O arquivo salvo está dentro do diretório `.kiro/specs/`
- O arquivo é um arquivo markdown (`.md`)
- O arquivo não está dentro de `specs/archive/`

## Instruções

- Verificar se a spec tem todas as seções obrigatórias baseado no seu tipo:
  - Para specs de feature (requirements.md): Resumo, Critérios de aceite, Restrições
  - Para specs de bugfix (bugfix.md): Passos de reprodução, Comportamento esperado, Comportamento atual, Causa raiz
  - Para docs de design (design.md): Abordagem, Componentes afetados, Riscos, Estratégia de rollback
  - Para arquivos de tarefas (tasks.md): Pelo menos uma tarefa com Descrição, Arquivos, Critérios de conclusão, Mensagem de commit
- Se critérios de aceite ou critérios de conclusão existem, verificar se cada um é específico e testável — sinalizar critérios vagos como "funciona corretamente" ou "é rápido"
- Se a spec toca banco de dados (menciona migration, ALTER, nova tabela/coluna), verificar se uma estratégia de rollback está documentada
- Se a spec toca código compartilhado ou APIs públicas, verificar se riscos estão listados
- Reportar seções ausentes como avisos, não erros — sugerir o que adicionar
