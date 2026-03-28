---
description: Verificar pré-condições antes de iniciar uma tarefa de spec
event: on_task_start
---

## Condições

- Uma tarefa de uma spec em `.kiro/specs/` está prestes a ser executada
- O arquivo de tarefas (tasks.md) existe e tem entradas estruturadas

## Instruções

- Ler a entrada da tarefa atual em tasks.md
- Verificar se a tarefa tem critérios de conclusão definidos — se ausentes, pedir ao usuário para defini-los antes de prosseguir
- Verificar se a tarefa tem dependências de outras tarefas — se essas tarefas não estão marcadas como completas, alertar o usuário
- Se a tarefa menciona mudanças de banco (migration, ALTER, nova tabela), verificar se a estratégia de rollback está documentada em design.md
- Se a tarefa toca arquivos em caminhos de código compartilhado (service/, model/, repository/), sinalizar como maior risco e lembrar o usuário de verificar o que mais depende desses arquivos
- Ler `.kiro/state/RISKS.md` e exibir quaisquer riscos abertos relevantes para o escopo desta tarefa
