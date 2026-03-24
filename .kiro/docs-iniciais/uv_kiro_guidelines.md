# Regras Obrigatórias: Uso do uv no Projeto Python (Windows 11 Pro)

## Diretriz Principal

Use SEMPRE `uv` como ferramenta padrão para:

- gerenciamento de ambiente virtual
- execução de scripts
- gerenciamento de dependências

NÃO utilize diretamente:

- pip
- python -m venv
- poetry
- pip-tools

---

## 1. Ambiente Python

- Sempre fixe a versão do Python do projeto:
  
  ```powershell
  uv python pin 3.12
  ```

- Sempre crie o ambiente virtual com `uv`:
  
  ```powershell
  uv venv --python 3.12
  ```

- O ambiente virtual DEVE estar em `.venv/`

---

## 2. Execução de Código

- SEMPRE use `uv run` para executar qualquer código Python:

```powershell
uv run main.py
```

```powershell
uv run -m package.module
```

- Para ferramentas:
  
  ```powershell
  uv run pytest
  uv run ruff check .
  ```

- NÃO use:
  
  ```powershell
  python main.py
  ```

---

## 3. Dependências

### Regra obrigatória

Toda dependência DEVE ser declarada no `pyproject.toml`.

### Adicionar dependências

- Produção:
  
  ```powershell
  uv add fastapi
  ```

- Desenvolvimento:
  
  ```powershell
  uv add --dev pytest ruff
  ```

- NÃO usar:
  
  ```powershell
  uv pip install <pacote>
  pip install <pacote>
  ```

---

## 4. Sincronização do Ambiente

Após qualquer alteração ou clone do projeto:

```powershell
uv sync
```

---

## 5. Separação de Dependências

- Use grupos:

```powershell
uv add --dev pytest
uv add --group lint ruff
uv add --group docs mkdocs
```

- NÃO misture dependências de produção com desenvolvimento.

---

## 6. Uso do uv pip (restrito)

Use `uv pip` APENAS quando:

- estiver lidando com projeto legado
- houver necessidade explícita de `requirements.txt`

Caso contrário: NÃO usar.

---

## 7. Fluxo padrão do projeto

Sempre seguir esta sequência:

```powershell
uv init
uv python pin 3.12
uv add <dependências>
uv sync
uv run <comando>
```

---

## 8. Windows (PowerShell)

Se precisar ativar manualmente o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Preferir sempre `uv run` ao invés de ativação manual.

---

## 9. Anti-padrões (PROIBIDO)

- Usar pip diretamente
- Executar scripts sem `uv run`
- Instalar dependências fora do `pyproject.toml`
- Não versionar `uv.lock`
- Misturar dependências sem grupos

---

## 10. Regra de Ouro

Se existir uma forma de fazer algo com `uv`, use `uv`.
