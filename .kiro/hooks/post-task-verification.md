---
description: Verificar conclusão da tarefa após execução
event: on_task_complete
---

## Condições

- Uma tarefa de uma spec em `.kiro/specs/` acabou de ser concluída
- O arquivo de tarefas (tasks.md) existe com entradas estruturadas

## Instruções

- Ler a entrada da tarefa concluída em tasks.md
- Verificar cada critério de conclusão — confirmar que foi realmente satisfeito
- Comparar os arquivos listados na tarefa com os arquivos realmente modificados na working tree — sinalizar mudanças inesperadas ou mudanças esperadas ausentes
- Se a tarefa alterou comportamento (não apenas refatoração), verificar se existe um teste que cobre a mudança
- Verificar se `.kiro/state/CHANGELOG_AI.md` tem uma entrada para esta tarefa — se não, lembrar o usuário de adicionar
- Se a tarefa foi a última da spec, sugerir rodar o agente verificador para uma checagem completa de entrega
