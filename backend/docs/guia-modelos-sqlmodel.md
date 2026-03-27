# Guia: Criando Tabelas e Entidades com SQLModel

Este guia explica como criar modelos de dados (entidades) no backend usando SQLModel, que unifica SQLAlchemy + Pydantic em uma única classe.

---

## Estrutura de Arquivos

Crie seus modelos dentro de `backend/src/models/`. Cada domínio pode ter seu próprio arquivo:

```
backend/src/
├── models/
│   ├── __init__.py       # Exporta todos os modelos
│   ├── commit.py         # Exemplo: modelo de commits
│   └── pull_request.py   # Exemplo: modelo de PRs
├── database.py           # Engine e sessão (já configurado)
└── main.py               # Aplicação FastAPI
```

---

## Criando um Modelo

Um modelo SQLModel é uma classe Python que define tanto a tabela no banco quanto o schema de validação da API.

```python
# backend/src/models/commit.py
from datetime import datetime

from sqlmodel import Field, SQLModel


class Commit(SQLModel, table=True):
    """Representa um commit do GitHub."""

    id: int | None = Field(default=None, primary_key=True)
    sha: str = Field(index=True, max_length=40)
    message: str
    author: str
    repo: str = Field(index=True)
    committed_at: datetime
    additions: int = Field(default=0)
    deletions: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
```

### Pontos importantes

- `table=True` indica que essa classe gera uma tabela no SQLite
- `Field(primary_key=True)` com `default=None` faz o ID ser autoincrement
- `Field(index=True)` cria índice para buscas mais rápidas
- Tipos Python padrão são mapeados automaticamente: `str` → TEXT, `int` → INTEGER, `datetime` → TIMESTAMP

---

## Registrando o Modelo

Para que o `create_db_and_tables()` no startup crie a tabela, o modelo precisa ser importado antes da chamada. Exporte no `__init__.py`:

```python
# backend/src/models/__init__.py
from src.models.commit import Commit

__all__ = ["Commit"]
```

E importe no `main.py` (basta o import, não precisa usar):

```python
# backend/src/main.py (adicionar no topo, após os imports existentes)
from src.models import Commit  # noqa: F401 — registra o modelo no metadata
```

Ao iniciar a aplicação, a tabela será criada automaticamente.

---

## Schemas de Request/Response

Use modelos SQLModel **sem** `table=True` para validação de entrada/saída na API:

```python
# backend/src/models/commit.py

class CommitCreate(SQLModel):
    """Schema para criação de commit (request body)."""

    sha: str
    message: str
    author: str
    repo: str
    committed_at: datetime
    additions: int = 0
    deletions: int = 0


class CommitRead(SQLModel):
    """Schema para leitura de commit (response)."""

    id: int
    sha: str
    message: str
    author: str
    repo: str
    committed_at: datetime
    additions: int
    deletions: int
    created_at: datetime
```

---

## Usando nos Endpoints

```python
# backend/src/main.py
from fastapi import Depends
from sqlmodel import Session, select

from src.database import get_session
from src.models.commit import Commit, CommitCreate, CommitRead


@app.post("/commits", response_model=CommitRead)
def create_commit(commit: CommitCreate, session: Session = Depends(get_session)):
    db_commit = Commit.model_validate(commit)
    session.add(db_commit)
    session.commit()
    session.refresh(db_commit)
    return db_commit


@app.get("/commits", response_model=list[CommitRead])
def list_commits(
    repo: str | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Commit)
    if repo:
        statement = statement.where(Commit.repo == repo)
    return session.exec(statement).all()
```

---

## Relacionamentos

Para relacionar tabelas, use `Relationship`:

```python
from sqlmodel import Field, Relationship, SQLModel


class Repository(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    full_name: str

    commits: list["Commit"] = Relationship(back_populates="repository")


class Commit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sha: str = Field(index=True, max_length=40)
    message: str
    repo_id: int = Field(foreign_key="repository.id")

    repository: Repository = Relationship(back_populates="commits")
```

---

## Campos Opcionais e Valores Padrão

```python
from sqlmodel import Field, SQLModel


class Metric(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    value: float
    description: str | None = None          # campo opcional (nullable)
    is_active: bool = Field(default=True)   # valor padrão
```

---

## Checklist para Novo Modelo

1. Criar arquivo em `backend/src/models/`
2. Definir classe com `SQLModel, table=True`
3. Exportar no `backend/src/models/__init__.py`
4. Importar no `main.py` para registrar no metadata
5. Criar schemas `Create` e `Read` (sem `table=True`) para a API
6. Rodar a aplicação — tabela é criada automaticamente no startup

---

## Referências

- [SQLModel docs](https://sqlmodel.tiangolo.com/)
- [SQLModel + FastAPI tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/)
