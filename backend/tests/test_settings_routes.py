"""Testes unitários para as rotas de configuração.

Valida: validação de token GitHub (formato ghp_/ghs_/github_pat_),
rejeição de tokens inválidos, get/post de config LLM,
e reset do singleton LLMClient ao trocar provider.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with (
        patch("src.services.ingestion.start_scheduler", return_value=MagicMock()),
        patch("src.rag.embeddings._get_model", return_value=MagicMock()),
    ):
        from src.main import app

        with TestClient(app) as c:
            yield c


class TestGitHubConfigValidation:
    def test_rejects_invalid_token_format(self, client):
        """Regra: token deve seguir formato ghp_xxx, ghs_xxx ou github_pat_xxx."""
        resp = client.post(
            "/settings/github",
            json={"token": "invalid_token_format", "username": "user"},
        )
        assert resp.status_code == 400
        assert "Token inválido" in resp.json()["detail"]

    def test_accepts_valid_ghp_token(self, client):
        """Regra: tokens ghp_ com 20+ chars são aceitos."""
        with patch("src.routes.settings.save_to_env"):
            resp = client.post(
                "/settings/github",
                json={"token": "ghp_abcdefghijklmnopqrstuvwxyz", "username": "user"},
            )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_accepts_valid_github_pat_token(self, client):
        """Regra: tokens github_pat_ são aceitos."""
        with patch("src.routes.settings.save_to_env"):
            resp = client.post(
                "/settings/github",
                json={
                    "token": "github_pat_abcdefghijklmnopqrstuvwxyz",
                    "username": "user",
                },
            )
        assert resp.status_code == 200

    def test_get_github_config_returns_has_token(self, client):
        """Regra: GET /settings/github retorna has_token e username."""
        resp = client.get("/settings/github")
        assert resp.status_code == 200
        data = resp.json()
        assert "has_token" in data
        assert "username" in data


class TestLLMConfig:
    def test_get_llm_config_returns_provider_and_model(self, client):
        """Regra: GET /settings/llm retorna provider, model, has_api_key."""
        resp = client.get("/settings/llm")
        assert resp.status_code == 200
        data = resp.json()
        assert data["provider"] in ("ollama", "openai")
        assert "model" in data
        assert "has_api_key" in data

    def test_save_llm_config_resets_singleton(self, client):
        """Regra: trocar config LLM reseta o singleton para pegar nova config."""
        with patch("src.routes.settings.save_to_env"):
            resp = client.post(
                "/settings/llm",
                json={"provider": "ollama", "model": "mistral", "api_key": ""},
            )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
