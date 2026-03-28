# Documento de Requisitos — Estrutura Base do Projeto

## Introdução

Este documento define os requisitos para a configuração da estrutura base do projeto Dashboard de Produtividade Dev. O objetivo é garantir que todos os desenvolvedores do time possam clonar o repositório e começar a desenvolver sem bloqueios de setup, com dependências gerenciadas via `uv`, variáveis de ambiente documentadas, convenções de código definidas e aplicações (backend FastAPI e frontend Streamlit) executando localmente sem erros.

## Glossário

- **Backend**: Aplicação Python baseada em FastAPI localizada no diretório `backend/`, responsável pela API REST do projeto.
- **Frontend**: Aplicação Python baseada em Streamlit localizada no diretório `frontend/`, responsável pelo dashboard interativo.
- **UV**: Ferramenta de gerenciamento de dependências e ambientes virtuais Python utilizada como padrão obrigatório do projeto, substituindo pip, poetry e requirements.txt.
- **Pyproject_Toml**: Arquivo `pyproject.toml` que declara metadados do projeto e dependências Python, conforme PEP 621.
- **Env_Example**: Arquivo `.env.example` que documenta todas as variáveis de ambiente necessárias com valores placeholder, sem dados sensíveis.
- **Gitignore**: Arquivo `.gitignore` que define padrões de arquivos e diretórios excluídos do controle de versão.
- **README**: Arquivo `README.md` na raiz do repositório com instruções de setup e execução do projeto.
- **Scripts_Dir**: Diretório `scripts/` destinado a scripts utilitários de automação do projeto.
- **Loguru**: Biblioteca Python de logging utilizada como padrão em todo o Backend.
- **PEP_8**: Guia de estilo de código Python (PEP 8) adotado como convenção obrigatória do projeto.

## Requisitos

### Requisito 1: Estrutura de Pastas do Repositório

**User Story:** Como desenvolvedor do time, quero que o repositório tenha uma estrutura de pastas padronizada, para que eu saiba onde encontrar e colocar cada tipo de arquivo.

#### Critérios de Aceite

1. THE Repositório SHALL conter os diretórios `backend/src/`, `backend/docs/`, `backend/tests/`, `frontend/src/`, `frontend/docs/`, `frontend/tests/` e `scripts/`.
2. THE Backend SHALL conter um arquivo `__init__.py` dentro de `backend/src/` para configurá-lo como pacote Python.
3. THE Frontend SHALL conter um arquivo `__init__.py` dentro de `frontend/src/` para configurá-lo como pacote Python.

### Requisito 2: Gerenciamento de Dependências do Backend com UV

**User Story:** Como desenvolvedor do time, quero que o backend tenha suas dependências declaradas em `pyproject.toml` e gerenciadas via `uv`, para que eu possa instalar tudo com um único comando.

#### Critérios de Aceite

1. THE Backend SHALL conter um arquivo Pyproject_Toml na raiz do diretório `backend/` declarando o nome do projeto, versão e versão do Python (3.12).
2. THE Pyproject_Toml do Backend SHALL declarar as dependências de produção: fastapi, uvicorn, loguru, python-dotenv, langchain, chromadb, aisuite e sqlite-utils.
3. THE Pyproject_Toml do Backend SHALL declarar as dependências de desenvolvimento: pytest, ruff.
4. WHEN um desenvolvedor executar `uv sync` dentro do diretório `backend/`, THE UV SHALL instalar todas as dependências declaradas no Pyproject_Toml sem erros.
5. THE Backend SHALL fixar a versão do Python em 3.12 via arquivo `.python-version`.

### Requisito 3: Gerenciamento de Dependências do Frontend com UV

**User Story:** Como desenvolvedor do time, quero que o frontend tenha suas dependências declaradas em `pyproject.toml` e gerenciadas via `uv`, para que eu possa instalar tudo com um único comando.

#### Critérios de Aceite

1. THE Frontend SHALL conter um arquivo Pyproject_Toml na raiz do diretório `frontend/` declarando o nome do projeto, versão e versão do Python (3.12).
2. THE Pyproject_Toml do Frontend SHALL declarar as dependências de produção: streamlit, plotly, python-dotenv, requests.
3. THE Pyproject_Toml do Frontend SHALL declarar as dependências de desenvolvimento: pytest, ruff.
4. WHEN um desenvolvedor executar `uv sync` dentro do diretório `frontend/`, THE UV SHALL instalar todas as dependências declaradas no Pyproject_Toml sem erros.
5. THE Frontend SHALL fixar a versão do Python em 3.12 via arquivo `.python-version`.

### Requisito 4: Variáveis de Ambiente Documentadas

**User Story:** Como desenvolvedor do time, quero ter arquivos `.env.example` preenchidos com todas as variáveis necessárias, para que eu saiba quais configurações preciso definir antes de rodar o projeto.

#### Critérios de Aceite

1. THE Env_Example do Backend SHALL conter as variáveis: GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_GRAPHQL_URL, CHROMADB_PATH, SQLITE_DB_PATH, LOG_LEVEL, OLLAMA_BASE_URL, OLLAMA_MODEL, EMBEDDING_MODEL e APP_PORT.
2. THE Env_Example do Frontend SHALL conter as variáveis: BACKEND_API_URL e STREAMLIT_SERVER_PORT.
3. THE Env_Example do Backend SHALL conter valores placeholder descritivos para cada variável (exemplo: `GITHUB_TOKEN=seu_token_aqui`).
4. THE Env_Example do Frontend SHALL conter valores placeholder descritivos para cada variável (exemplo: `BACKEND_API_URL=http://localhost:8000`).

### Requisito 5: Proteção de Dados Sensíveis

**User Story:** Como desenvolvedor do time, quero que variáveis sensíveis nunca sejam commitadas no repositório, para que tokens e credenciais permaneçam seguros.

#### Critérios de Aceite

1. THE Gitignore SHALL conter regras para excluir arquivos `.env` do controle de versão.
2. THE Gitignore SHALL conter regras para excluir diretórios `.venv/` e `__pycache__/` do controle de versão.
3. THE Gitignore SHALL conter regras para excluir arquivos de banco de dados SQLite (`*.db`, `*.sqlite`, `*.sqlite3`) do controle de versão.
4. THE Gitignore SHALL conter regras para excluir diretórios de dados do ChromaDB (`chroma_data/`) do controle de versão.

### Requisito 6: README com Instruções de Setup Local

**User Story:** Como desenvolvedor do time, quero um README atualizado com instruções claras de setup local, para que eu consiga rodar o projeto seguindo um passo a passo.

#### Critérios de Aceite

1. THE README SHALL conter uma descrição do projeto Dashboard de Produtividade Dev.
2. THE README SHALL conter a lista de pré-requisitos: Python 3.12, uv, Ollama.
3. THE README SHALL conter instruções passo a passo para configurar o Backend (clonar, copiar `.env.example` para `.env`, executar `uv sync`, executar `uv run uvicorn`).
4. THE README SHALL conter instruções passo a passo para configurar o Frontend (copiar `.env.example` para `.env`, executar `uv sync`, executar `uv run streamlit run`).
5. THE README SHALL conter a estrutura de diretórios do projeto.
6. THE README SHALL conter a stack técnica utilizada (FastAPI, Streamlit, Plotly, ChromaDB, Ollama, loguru, aisuite, SQLite).

### Requisito 7: Aplicação Backend Executável Localmente

**User Story:** Como desenvolvedor do time, quero que o backend rode localmente com uvicorn sem erros, para que eu possa validar que o setup está correto.

#### Critérios de Aceite

1. THE Backend SHALL conter um arquivo `backend/src/main.py` com uma aplicação FastAPI mínima que responda a requisições HTTP.
2. WHEN um desenvolvedor executar `uv run uvicorn src.main:app --reload` dentro do diretório `backend/`, THE Backend SHALL iniciar o servidor na porta configurada sem erros.
3. WHEN o Backend estiver em execução, THE Backend SHALL responder com status HTTP 200 e uma mensagem JSON na rota `/health`.
4. THE Backend SHALL configurar Loguru como sistema de logging padrão na inicialização da aplicação.

### Requisito 8: Aplicação Frontend Executável Localmente

**User Story:** Como desenvolvedor do time, quero que o frontend rode localmente com Streamlit sem erros, para que eu possa validar que o setup está correto.

#### Critérios de Aceite

1. THE Frontend SHALL conter um arquivo `frontend/src/app.py` com uma aplicação Streamlit mínima que renderize uma página inicial.
2. WHEN um desenvolvedor executar `uv run streamlit run src/app.py` dentro do diretório `frontend/`, THE Frontend SHALL iniciar o servidor Streamlit sem erros.
3. WHEN o Frontend estiver em execução, THE Frontend SHALL exibir o título "Dashboard de Produtividade Dev" na página inicial.

### Requisito 9: Convenções de Código

**User Story:** Como desenvolvedor do time, quero que as convenções de código estejam configuradas desde o início, para que todo o código siga o mesmo padrão.

#### Critérios de Aceite

1. THE Backend SHALL conter configuração do Ruff no Pyproject_Toml com regras baseadas em PEP_8.
2. THE Frontend SHALL conter configuração do Ruff no Pyproject_Toml com regras baseadas em PEP_8.
3. WHEN um desenvolvedor executar `uv run ruff check .` dentro do diretório `backend/` ou `frontend/`, THE Ruff SHALL validar o código sem reportar violações nos arquivos iniciais.
