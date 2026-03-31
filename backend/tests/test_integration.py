"""Testes de integração do backend.

Validam fluxos completos que cruzam múltiplas camadas:
rotas → serviços → modelos → respostas HTTP.

Mínimo 5 testes de integração que validam regras reais do sistema.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """TestClient com dependências pesadas mockadas."""
    with (
        patch("src.services.ingestion.start_scheduler", return_value=MagicMock()),
        patch("src.rag.embeddings._get_model", return_value=MagicMock()),
    ):
        from src.main import app

        with TestClient(app) as c:
            yield c


# ---------------------------------------------------------------------------
# Integração 1: POST /insights com query vazia retorna 400
# Fluxo: rota insights → validação de input → HTTP 400
# ---------------------------------------------------------------------------
class TestInsightsValidation:
    def test_empty_query_returns_400(self, client):
        """Regra: query vazia no chat RAG deve ser rejeitada com 400."""
        resp = client.post("/insights", json={"query": ""})
        assert resp.status_code == 400
        assert "vazia" in resp.json()["detail"].lower()

    def test_missing_query_field_returns_422(self, client):
        """Regra: payload sem campo query retorna 422 (validation error)."""
        resp = client.post("/insights", json={})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Integração 2: POST /insights com pipeline RAG completo (mockado)
# Fluxo: rota → RAGPipeline → embedder → vector_store → LLM → Insight
# ---------------------------------------------------------------------------
class TestInsightsPipelineIntegration:
    def test_valid_query_returns_insight_with_all_fields(self, client):
        """Regra: insight retornado deve ter summary, evidence,
        recommendation, sources."""
        mock_pipeline = MagicMock()

        from src.rag.models import Insight

        mock_insight = Insight(
            summary="Você fez 10 commits essa semana",
            evidence="Commits no repo user/app",
            recommendation="Mantenha o ritmo",
            sources=["Commit abc: feat login"],
        )
        mock_pipeline.query = AsyncMock(return_value=mock_insight)

        with patch("src.routes.insights.RAGPipeline", return_value=mock_pipeline):
            resp = client.post("/insights", json={"query": "O que fiz essa semana?"})

        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        assert "evidence" in data
        assert "recommendation" in data
        assert "sources" in data
        assert data["summary"] == "Você fez 10 commits essa semana"


# ---------------------------------------------------------------------------
# Integração 3: GET /export/csv retorna CSV válido com métricas
# Fluxo: rota export → MetricsService → CSV streaming response
# ---------------------------------------------------------------------------
class TestExportCSVIntegration:
    def test_csv_export_contains_metric_headers(self, client):
        """Regra: export CSV contém cabeçalho 'metrica,valor' e dados reais."""
        mock_metrics = {
            "total_commits": 42,
            "total_prs": 10,
            "prs_merged": 8,
            "issues_fechadas": 5,
            "tempo_medio_merge_horas": 3.2,
            "hot_repos": [{"repo": "user/app", "commits": 20}],
            "periodo_dias": 90,
        }
        mock_svc = MagicMock()
        mock_svc.calculate = AsyncMock(return_value=mock_metrics)

        with patch("src.routes.export.MetricsService", return_value=mock_svc):
            resp = client.get("/export/csv")

        assert resp.status_code == 200
        assert resp.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in resp.headers.get("content-disposition", "")
        body = resp.text
        assert "metrica,valor" in body
        assert "total_commits" in body
        assert "42" in body


# ---------------------------------------------------------------------------
# Integração 4: POST /ingest dispara ingestão em background
# Fluxo: rota metrics → BackgroundTasks → run_ingestion
# ---------------------------------------------------------------------------
class TestIngestTriggerIntegration:
    def test_ingest_returns_started_status(self, client):
        """Regra: POST /ingest retorna status=started e dispara background task."""
        with patch("src.routes.metrics.run_ingestion", new_callable=AsyncMock):
            resp = client.post("/ingest")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "started"
        assert (
            "background" in data["message"].lower()
            or "iniciada" in data["message"].lower()
        )

    def test_ingest_status_returns_expected_fields(self, client):
        """Regra: GET /ingest/status retorna campos de monitoramento."""
        resp = client.get("/ingest/status")
        assert resp.status_code == 200
        data = resp.json()
        for field in ["running", "step", "progress", "total", "logs"]:
            assert field in data, f"Campo '{field}' ausente no status de ingestão"


# ---------------------------------------------------------------------------
# Integração 5: Fluxo completo GitHub → Métricas via API
# Fluxo: rota /metrics → MetricsService → GitHubCollector (mock) → KPIs
# ---------------------------------------------------------------------------
class TestMetricsEndpointIntegration:
    def test_metrics_endpoint_returns_kpis(self, client):
        """Regra: GET /metrics retorna KPIs calculados a partir de dados GitHub."""
        from datetime import datetime, timezone

        mock_commits = [
            MagicMock(
                date=datetime(2026, 3, 20, tzinfo=timezone.utc),
                repository="user/repo",
            ),
        ]
        mock_prs = [
            MagicMock(
                created_at=datetime(2026, 3, 18, tzinfo=timezone.utc),
                merged_at=datetime(2026, 3, 19, tzinfo=timezone.utc),
                state="MERGED",
            ),
        ]
        mock_issues = []

        mock_collector = MagicMock()
        mock_collector.fetch_commits = AsyncMock(return_value=mock_commits)
        mock_collector.fetch_pull_requests = AsyncMock(return_value=mock_prs)
        mock_collector.fetch_issues = AsyncMock(return_value=mock_issues)

        with (
            patch("src.services.metrics.settings") as mock_settings,
            patch("src.services.metrics.GitHubCollector", return_value=mock_collector),
            patch("src.services.metrics._cache", {}),
        ):
            mock_settings.github_token = "ghp_test"
            mock_settings.ingestion_days_back = 90
            resp = client.get("/metrics")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total_commits"] == 1
        assert data["total_prs"] == 1
        assert data["prs_merged"] == 1
        assert "hot_repos" in data


# ---------------------------------------------------------------------------
# Integração 6: Health check detalhado verifica todos os serviços
# Fluxo: rota /health/detailed → ChromaDB check + GitHub check + LLM check
# ---------------------------------------------------------------------------
class TestHealthDetailedIntegration:
    def test_health_detailed_returns_all_checks(self, client):
        """Regra: /health/detailed retorna status de api, chromadb, github, llm."""
        with (
            patch(
                "src.routes.health._check_chromadb",
                new_callable=AsyncMock,
                return_value="ok",
            ),
            patch(
                "src.routes.health._check_github",
                new_callable=AsyncMock,
                return_value="not_configured",
            ),
            patch(
                "src.routes.health._check_llm",
                new_callable=AsyncMock,
                return_value="error: ollama not running",
            ),
        ):
            resp = client.get("/health/detailed")

        assert resp.status_code == 200
        data = resp.json()
        assert "checks" in data
        checks = data["checks"]
        assert "api" in checks
        assert "chromadb" in checks
        assert "github" in checks
        assert "llm" in checks
        # Se algum check falha, status geral é "degraded"
        assert data["status"] == "degraded"

    def test_health_detailed_all_ok(self, client):
        """Regra: quando todos os serviços estão ok, status geral é 'ok'."""
        with (
            patch(
                "src.routes.health._check_chromadb",
                new_callable=AsyncMock,
                return_value="ok",
            ),
            patch(
                "src.routes.health._check_github",
                new_callable=AsyncMock,
                return_value="ok",
            ),
            patch(
                "src.routes.health._check_llm",
                new_callable=AsyncMock,
                return_value="ok",
            ),
        ):
            resp = client.get("/health/detailed")

        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
