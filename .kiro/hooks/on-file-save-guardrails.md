---
description: Verificar mudanças em arquivos críticos contra padrões de código e segurança
event: on_file_save
---

## Condições

- O arquivo salvo corresponde a qualquer um destes caminhos:
  - `**/migration/**` ou `**/db/**` (migrações de banco)
  - `**/security/**` ou `**/auth/**` (código relacionado a segurança)
  - `**/model/**` ou `**/entity/**` (modelos de domínio / entidades JPA)
  - `**/application*.yml` ou `**/application*.properties` (configuração)

## Instruções

- Para arquivos de migração de banco:
  - Alertar se a migração contém `DROP TABLE` ou `DROP COLUMN` sem um comentário explicando o motivo
  - Alertar se `CREATE INDEX` é usado sem `CONCURRENTLY` em uma tabela que provavelmente é grande
  - Alertar se uma coluna `NOT NULL` é adicionada sem um valor `DEFAULT`
- Para arquivos de segurança/auth:
  - Sinalizar qualquer string hardcoded que pareça credencial, token ou API key
  - Verificar se o tratamento de senha usa bcrypt ou algoritmo de hash forte, não MD5/SHA-1
  - Sinalizar anotações `@PermitAll` ou endpoint público — confirmar que são intencionais
- Para arquivos de model/entity:
  - Alertar se um campo é removido (pode quebrar queries existentes ou contratos de API)
  - Alertar se o tipo de um campo é alterado (pode requerer migração de dados)
- Para arquivos de configuração:
  - Sinalizar qualquer valor que pareça secret (senhas, chaves, tokens) — devem ser variáveis de ambiente
  - Alertar se o tamanho do pool de conexões do banco é alterado
- Manter alertas concisos — uma linha por problema, com caminho do arquivo e número da linha quando possível
