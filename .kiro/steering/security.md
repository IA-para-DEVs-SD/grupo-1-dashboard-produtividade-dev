---
description: Regras de segurança — auth, validação de input, secrets, scan de dependências
inclusion: auto
---

# Diretrizes de Segurança

## Autenticação e autorização
- Todos os endpoints requerem autenticação a menos que explicitamente marcados como públicos
- Aplicar autorização no servidor, nunca confiar apenas em verificações do lado do cliente
- Nunca armazenar senhas em texto plano — usar bcrypt ou equivalente

## Validação de input
- Validar todos os inputs na fronteira da API
- Rejeitar campos inesperados
- Sanitizar qualquer input renderizado em HTML (prevenção de XSS)
- Upload de arquivos: validar MIME type, aplicar limites de tamanho

## Prevenção de SQL injection
- Usar queries parametrizadas exclusivamente
- Nunca usar concatenação de strings em queries SQL

## Gestão de secrets
- Nunca commitar secrets, tokens, API keys ou credenciais no git
- Usar variáveis de ambiente ou gerenciador de secrets
- Se um secret foi commitado acidentalmente: rotacionar imediatamente

## Segurança de dependências
- Rodar scan de vulnerabilidades de dependências no CI
- CVEs críticas: corrigir em até 7 dias
- CVEs altas: corrigir em até 30 dias
