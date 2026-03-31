"""Testes unitários para o app FastAPI principal.

Valida: health check, CORS, correlation ID middleware, registro de rotas.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """Cria TestClient mockando dependências pesadas (scheduler, LLM, embeddings)."""
    with (
        patch("src.services.ingestion.start_scheduler", return_value=MagicMock()),
        patch("src.rag.embeddings._get_model", return_value=MagicMock()),
    ):
        from src.main import app

        with TestClient(app) as c:
            yield c


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_returns_ok_json(self, client):
        resp = client.get("/health")
        assert resp.json() == {"status": "ok"}


class TestCorrelationIdMiddleware:
    def test_response_contains_correlation_id_header(self, client):
        resp = client.get("/health")
        assert "X-Correlation-ID" in resp.headers
        assert len(resp.headers["X-Correlation-ID"]) == 8


class TestCORSMiddleware:
    def test_cors_allows_configured_origin(self, client):
        resp = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:8501",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert (
            resp.headers.get("access-control-allow-origin")
            == "http://localhost:8501"
        )


class TestRouterRegistration:
    """Verifica que todas as rotas documentadas estão registradas no app."""

    EXPECTED_PATHS = [
        "/health",
        "/health/detailed",
        "/github/status",
        "/insights",
        "/metrics",
        "/metrics/weekly",
        "/ingest",
        "/ingest/status",
        "/export/csv",
        "/export/pdf",
        "/settings/github",
        "/settings/llm",
    ]

    def test_all_expected_routes_registered(self, client):
        from src.main import app

        registered = {route.path for route in app.routes}
        for path in self.EXPECTED_PATHS:
            assert path in registered, f"Rota {path} não registrada no app"
