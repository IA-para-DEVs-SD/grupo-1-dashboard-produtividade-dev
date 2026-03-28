---
description: Detectar e registrar decisões arquiteturais em DECISIONS.md
event: manual
---

# Hook de Rastreamento de Decisões

## Condições
- Após uma sessão de planejamento onde escolhas de tecnologia ou padrões arquiteturais foram decididos
- Após uma implementação de tarefa que introduziu um novo padrão ou dependência
- Quando o usuário explicitamente diz "registrar esta decisão" ou "logar decisão"
- Após o agente planner produzir um design.md com escolhas arquiteturais

## Instruções

Escanear a sessão atual por decisões arquiteturais. Procurar por:
1. Escolhas de tecnologia (biblioteca A sobre biblioteca B, padrão X sobre padrão Y)
2. Decisões estruturais (onde colocar código, como organizar módulos)
3. Trade-offs discutidos (performance vs simplicidade, consistência vs flexibilidade)
4. Alternativas rejeitadas (o que foi considerado mas não escolhido, e por quê)

Para cada decisão encontrada, adicionar uma entrada em `.kiro/state/DECISIONS.md`:

```markdown
### YYYY-MM-DD — [Título curto da decisão]

**Contexto:** Por que esta decisão foi necessária.

**Decisão:** O que foi decidido.

**Alternativas consideradas:**
- Alternativa A — rejeitada porque...
- Alternativa B — rejeitada porque...

**Consequências:** O que isso significa daqui para frente.

**Spec:** [nome-da-spec] (se relacionada a uma spec específica)
```

Regras:
- Apenas adicionar — nunca modificar ou deletar decisões anteriores
- Ser específico — "escolheu eventos CDI sobre chamada direta de método" não "escolheu uma abordagem"
- Incluir as alternativas rejeitadas — sessões futuras precisam saber o que já foi considerado
- Se uma decisão contradiz uma anterior, notar explicitamente e explicar por quê
- Uma entrada por decisão — não agrupar decisões não relacionadas
