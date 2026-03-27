import os

from sqlmodel import Session, SQLModel, create_engine

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data.db")
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables() -> None:
    """Cria todas as tabelas definidas nos modelos SQLModel."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency do FastAPI para injetar sessão do banco."""
    with Session(engine) as session:
        yield session
