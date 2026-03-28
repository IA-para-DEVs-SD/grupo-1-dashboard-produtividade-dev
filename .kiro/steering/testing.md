---
description: Estratégia de testes — o que testar, como testar, expectativas de cobertura
inclusion: auto
---

# Diretrizes de Testes

## Estratégia de testes
- Testes unitários para toda lógica de negócio na camada de serviços
- Testes de integração para acesso a dados com banco real (Testcontainers ou equivalente)
- Testes de API para endpoints (validação de request/response)

## Expectativas de cobertura
- Novos métodos de serviço: 80%+ de cobertura de branches
- Correções de bugs: devem incluir teste de regressão que falha sem a correção
- Refatoração: todos os testes existentes devem passar sem modificação
- Código legado sem testes: adicionar teste de caracterização antes de modificar

## Estrutura dos testes
Use o padrão Arrange-Act-Assert. Nomeie testes descritivamente: `should_resultadoEsperado_when_condicao`.

## Dados de teste
- Use builders/factories para entidades de teste
- Nunca compartilhe estado mutável entre testes
- Nunca dependa de dados de outros testes

## O que NÃO testar
- Internos do framework (cascade do ORM, wiring de DI)
- Getters/setters
- Comportamento de bibliotecas de terceiros
