"""Testes de propriedade para arquivos .env.example do projeto.

Feature: project-base-setup
Property 1: Presença de variáveis obrigatórias nos arquivos .env.example
Property 2: Placeholders não-vazios nos arquivos .env.example

Valida: Requisitos 4.1, 4.2, 4.3, 4.4
"""

from pathlib import Path

from hypothesis import given, settings
from hypothesis.strategies import sampled_from

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

REQUIRED_VARS: dict[str, list[str]] = {
    "backend": [
        "GITHUB_TOKEN",
        "GITHUB_USERNAME",
        "LLM_PROVIDER",
        "LLM_MODEL",
        "CHROMA_PATH",
        "CHROMA_COLLECTION",
        "INGESTION_DAYS_BACK",
    ],
    "frontend": [
        "BACKEND_API_URL",
        "STREAMLIT_SERVER_PORT",
    ],
}

SUBPROJECT_VAR_PAIRS = [
    (subproject, var)
    for subproject, vars_ in REQUIRED_VARS.items()
    for var in vars_
]


def _parse_env_variables(env_path: Path) -> set[str]:
    """Parse variable names from a .env.example file."""
    variables: set[str] = set()
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            var_name = stripped.split("=", 1)[0].strip()
            variables.add(var_name)
    return variables


@settings(max_examples=100)
@given(pair=sampled_from(SUBPROJECT_VAR_PAIRS))
def test_required_variables_present_in_env_example(pair: tuple[str, str]) -> None:
    """**Validates: Requirements 4.1, 4.2**

    Feature: project-base-setup
    Property 1: Presença de variáveis obrigatórias nos arquivos .env.example

    Para qualquer subprojeto (backend ou frontend) e para qualquer variável
    na lista de variáveis obrigatórias desse subprojeto, essa variável deve
    estar definida no arquivo .env.example correspondente.
    """
    subproject, variable = pair
    env_path = PROJECT_ROOT / subproject / ".env.example"

    assert env_path.exists(), (
        f"Arquivo {subproject}/.env.example não encontrado"
    )

    defined_vars = _parse_env_variables(env_path)

    assert variable in defined_vars, (
        f"Variável obrigatória '{variable}' não encontrada em "
        f"{subproject}/.env.example. "
        f"Variáveis encontradas: {sorted(defined_vars)}"
    )


# ---------------------------------------------------------------------------
# Property 2: Placeholders não-vazios nos arquivos .env.example
# ---------------------------------------------------------------------------

ENV_EXAMPLE_FILES = [
    PROJECT_ROOT / "backend" / ".env.example",
    PROJECT_ROOT / "frontend" / ".env.example",
]


def _collect_file_variable_pairs() -> list[tuple[str, str]]:
    """Collect all (file_path, variable_name) pairs from .env.example files."""
    pairs: list[tuple[str, str]] = []
    for env_path in ENV_EXAMPLE_FILES:
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                var_name = stripped.split("=", 1)[0].strip()
                pairs.append((str(env_path), var_name))
    return pairs


FILE_VAR_PAIRS = _collect_file_variable_pairs()


@settings(max_examples=100)
@given(pair=sampled_from(FILE_VAR_PAIRS))
def test_env_example_placeholders_not_empty(pair: tuple[str, str]) -> None:
    """**Validates: Requirements 4.3, 4.4**

    Feature: project-base-setup
    Property 2: Placeholders não-vazios nos arquivos .env.example

    Para qualquer variável definida em qualquer arquivo .env.example do
    projeto, o valor atribuído (placeholder) não deve ser uma string vazia —
    deve conter um valor descritivo que indique ao desenvolvedor o que preencher.
    """
    file_path, variable = pair
    env_path = Path(file_path)

    assert env_path.exists(), f"Arquivo {file_path} não encontrado"

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            var_name, value = stripped.split("=", 1)
            if var_name.strip() == variable:
                assert value.strip() != "", (
                    f"Variável '{variable}' em {env_path.name} tem "
                    f"placeholder vazio. Cada variável deve ter um valor "
                    f"descritivo após o '='."
                )
                return

    assert False, f"Variável '{variable}' não encontrada em {file_path}"
