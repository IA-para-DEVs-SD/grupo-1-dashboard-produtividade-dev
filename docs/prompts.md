# Prompts utilizados no projeto

Registro dos prompts usados durante o desenvolvimento do projeto com auxílio de IA.

---

## 1. Atualizar projeto com repositório remoto

```
atualize o projeto de acordo com o repositório remoto
```

Resultado: sincronização da branch local com `origin`, trazendo novas branches remotas (`feat/criar-readme`, `feature/fluxograma`, `feature/specs-edemilson`) e atualizações em `main` e `develop`.

---

## 2. Refatorar projeto conforme diretrizes

```
refatore o projeto de acordo com as diretrizes:

Estrutura padrão de repositórios

Padrão de nomenclatura dos repositórios de projetos
Nome grupo + Nome do projeto: Exemplo: "grupo-x-nome-projeto"
Não utilizar caracteres especiais além do hífen
Texto sempre em minúsculo

Padrão de nomenclatura dos repositórios de atividades
Nome grupo + Atividades + Nome aluno: Exemplo: "grupo-x-atividades-fulano-sobrenome"
Não utilizar caracteres especiais além do hífen
Texto sempre em minúsculo

Padrão do Gitflow
Branch principal: main
Branch desenvolvimento: develop
Branch de novas funcionalidades: feature/issue-xxx

Padrão do commit semântico
"tipo: breve descrição
descrição mais detalhada (opcional)"
Tipos:
feat: Nova funcionalidade
docs: Documentações
fix: Correções
refactor: Refatorações
tests: Testes unitários, etc

Padrão de nomenclatura dos boards / projetos
Identificação do Grupo + Nome do Projeto
Exemplo: "Grupo X - Nome Projeto"

Padrão de tópicos do README
Nome do Projeto
Breve descrição do projeto
Sumário de documentações
Tecnologias utilizadas
Instruções de instalação / uso
Integrantes do grupo
```

Resultado: `main` atualizada, branch `develop` criada localmente, branch `feature/issue-001` criada a partir de `develop`, README refatorado com todos os tópicos obrigatórios e commit semântico aplicado.

---

## 3. Abrir Pull Request

```
Pode seguir com o PR
```

Resultado: push da branch `feature/issue-001` para o remoto e tentativa de abertura do PR via `gh` CLI. Como o CLI não estava instalado, o PR foi aberto manualmente pelo link gerado pelo GitHub.

---

## 4. Registrar prompts do projeto

```
Olá, crie uma pasta docs no diretório e um arquivo em .md e registre todos os prompts que usamos até agora para gerar o projeto
```

Resultado: criação deste arquivo em `docs/prompts.md`.
