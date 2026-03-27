"""Testes unitários de validação estrutural do projeto.

Verifica a existência de diretórios obrigatórios, arquivos de configuração,
conteúdo de .python-version, padrões no .gitignore e configuração do Ruff.

Valida: Requisitos 1.1, 1.2, 1.3, 2.5, 3.5, 5.1–5.4, 9.1, 9.2
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Req 1.1 — Diretórios obrigatórios
# ---------------------------------------------------------------------------

REQUIRED_DIRS = [
    "backend/src",
    "backend/tests",
    "backend/docs",
    "frontend/src",
    "frontend/tests",
    "frontend/docs",
    "scripts",
]


@pytest.mark.parametrize("rel_dir", REQUIRED_DIRS)
def test_required_directory_exists(rel_dir: str) -> None:
    """Verifica existência de todos os diretórios obrigatórios (Req 1.1)."""
    path = PROJECT_ROOT / rel_dir
    assert path.is_dir(), f"Diretório obrigatório ausente: {rel_dir}"


# ---------------------------------------------------------------------------
# Req 1.2, 1.3 — __init__.py em backend/src/ e frontend/src/
# ---------------------------------------------------------------------------

INIT_PY_LOCATIONS = [
    "backend/src/__init__.py",
    "frontend/src/__init__.py",
]


@pytest.mark.parametrize("rel_path", INIT_PY_LOCATIONS)
def test_init_py_exists(rel_path: str) -> None:
    """Verifica existência de __init__.py nos pacotes src (Req 1.2, 1.3)."""
    path = PROJECT_ROOT / rel_path
    assert path.is_file(), f"Arquivo ausente: {rel_path}"


# ---------------------------------------------------------------------------
# Req 2.5, 3.5 — .python-version contém "3.12"
# ---------------------------------------------------------------------------

PYTHON_VERSION_FILES = [
    "backend/.python-version",
    "frontend/.python-version",
]


@pytest.mark.parametrize("rel_path", PYTHON_VERSION_FILES)
def test_python_version_contains_3_12(rel_path: str) -> None:
    """Verifica conteúdo de .python-version em ambos subprojetos (Req 2.5, 3.5)."""
    path = PROJECT_ROOT / rel_path
    assert path.is_file(), f"Arquivo ausente: {rel_path}"
    content = path.read_text(encoding="utf-8").strip()
    assert "3.12" in content, (
        f"{rel_path} deveria conter '3.12', mas contém: '{content}'"
    )


# ---------------------------------------------------------------------------
# Req 5.1–5.4 — Padrões obrigatórios no .gitignore
# ---------------------------------------------------------------------------

GITIGNORE_PATTERNS = [
    ".env",
    ".venv/",
    "__pycache__/",
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "chroma_data/",
]


@pytest.mark.parametrize("pattern", GITIGNORE_PATTERNS)
def test_gitignore_contains_pattern(pattern: str) -> None:
    """Verifica presença de padrões obrigatórios no .gitignore (Req 5.1–5.4)."""
    gitignore_path = PROJECT_ROOT / ".gitignore"
    assert gitignore_path.is_file(), ".gitignore não encontrado na raiz"
    content = gitignore_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    assert pattern in lines, (
        f"Padrão '{pattern}' não encontrado no .gitignore"
    )


# ---------------------------------------------------------------------------
# Req 9.1, 9.2 — Seção [tool.ruff] nos pyproject.toml
# ---------------------------------------------------------------------------

PYPROJECT_FILES = [
    "backend/pyproject.toml",
    "frontend/pyproject.toml",
]


@pytest.mark.parametrize("rel_path", PYPROJECT_FILES)
def test_pyproject_contains_ruff_config(rel_path: str) -> None:
    """Verifica seção [tool.ruff] nos pyproject.toml (Req 9.1, 9.2)."""
    path = PROJECT_ROOT / rel_path
    assert path.is_file(), f"Arquivo ausente: {rel_path}"
    content = path.read_text(encoding="utf-8")
    assert "[tool.ruff]" in content, (
        f"Seção [tool.ruff] não encontrada em {rel_path}"
    )
