"""Serviço para persistência de configurações no arquivo .env."""

import os

from loguru import logger

ENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")


def save_to_env(updates: dict[str, str]) -> None:
    """Persiste atualizações de configuração no arquivo .env.

    Lê o arquivo existente, aplica as atualizações e reescreve.
    Cria o arquivo se não existir.
    """
    existing: dict[str, str] = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    existing[key] = val

    existing.update(updates)

    with open(ENV_PATH, "w") as f:
        for key, val in existing.items():
            f.write(f"{key}={val}\n")

    logger.bind(cid="settings").info(
        f"Configurações salvas no .env: {list(updates.keys())}"
    )
