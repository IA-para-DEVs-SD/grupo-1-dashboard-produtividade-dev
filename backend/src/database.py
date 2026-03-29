from sqlmodel import Session, SQLModel, create_engine

from src.config import settings

DATABASE_URL = f"sqlite:///{settings.sqlite_db_path}"

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Cria todas as tabelas definidas nos modelos SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency do FastAPI para injetar sessão do banco."""
    with Session(engine) as session:
        yield session
