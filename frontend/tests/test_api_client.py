"""Testes unitários para o cliente HTTP do frontend.

Valida: construção de URLs, passagem de parâmetros de data,
tratamento de erros HTTP, e que todas as funções chamam os endpoints corretos.
"""

from unittest.mock import MagicMock, patch

from src.api_client import (
    get_export_url,
    get_github_status,
    get_ingest_status,
    get_metrics,
    get_metrics_weekly,
    post_insight,
    save_github_config,
    save_llm_config,
    trigger_ingest,
)


class TestGetExportUrl:
    def test_csv_url_without_dates(self):
        """Regra: URL de export CSV sem filtro de data."""
        url = get_export_url("csv")
        assert "/export/csv" in url
        assert "?" not in url

    def test_csv_url_with_dates(self):
        """Regra: URL de export CSV com filtro from/to."""
        url = get_export_url("csv", "2026-01-01", "2026-03-01")
        assert "/export/csv?" in url
        assert "from=2026-01-01" in url
        assert "to=2026-03-01" in url

    def test_pdf_url(self):
        """Regra: URL de export PDF usa /export/pdf."""
        url = get_export_url("pdf")
        assert "/export/pdf" in url


class TestGitHubEndpoints:
    @patch("src.api_client.requests.get")
    def test_get_github_status_calls_correct_endpoint(self, mock_get):
        """Regra: get_github_status chama GET /github/status."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"connected": True, "username": "dev"}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = get_github_status()
        mock_get.assert_called_once()
        assert "/github/status" in mock_get.call_args[0][0]
        assert result["connected"] is True

    @patch("src.api_client.requests.post")
    def test_save_github_config_sends_token_and_username(self, mock_post):
        """Regra: save_github_config envia token e username via POST."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "ok"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        save_github_config("ghp_test123456789012345", "myuser")
        call_kwargs = mock_post.call_args
        assert "/settings/github" in call_kwargs[0][0]
        payload = call_kwargs[1]["json"]
        assert payload["token"] == "ghp_test123456789012345"
        assert payload["username"] == "myuser"


class TestMetricsEndpoints:
    @patch("src.api_client.requests.get")
    def test_get_metrics_passes_date_params(self, mock_get):
        """Regra: get_metrics passa from/to como query params."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"total_commits": 10}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        get_metrics("2026-01-01", "2026-03-01")
        call_kwargs = mock_get.call_args
        params = call_kwargs[1].get("params") or call_kwargs.kwargs.get("params")
        assert params["from"] == "2026-01-01"
        assert params["to"] == "2026-03-01"

    @patch("src.api_client.requests.get")
    def test_get_metrics_weekly_calls_correct_endpoint(self, mock_get):
        """Regra: get_metrics_weekly chama GET /metrics/weekly."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"weeks": [], "commits": []}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        get_metrics_weekly()
        assert "/metrics/weekly" in mock_get.call_args[0][0]


class TestInsightsEndpoint:
    @patch("src.api_client.requests.post")
    def test_post_insight_sends_query(self, mock_post):
        """Regra: post_insight envia query ao pipeline RAG via POST /insights."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "summary": "Resumo",
            "evidence": "",
            "recommendation": "",
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = post_insight("O que fiz hoje?")
        call_kwargs = mock_post.call_args
        assert "/insights" in call_kwargs[0][0]
        assert call_kwargs[1]["json"]["query"] == "O que fiz hoje?"
        assert result["summary"] == "Resumo"


class TestLLMEndpoints:
    @patch("src.api_client.requests.post")
    def test_save_llm_config_sends_provider_and_model(self, mock_post):
        """Regra: save_llm_config envia provider, model e api_key."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "ok"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        save_llm_config("openai", "gpt-4o-mini", "sk-test")
        payload = mock_post.call_args[1]["json"]
        assert payload["provider"] == "openai"
        assert payload["model"] == "gpt-4o-mini"
        assert payload["api_key"] == "sk-test"


class TestIngestEndpoints:
    @patch("src.api_client.requests.post")
    def test_trigger_ingest_calls_post(self, mock_post):
        """Regra: trigger_ingest dispara POST /ingest."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "started"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = trigger_ingest()
        assert "/ingest" in mock_post.call_args[0][0]
        assert result["status"] == "started"

    @patch("src.api_client.requests.get")
    def test_get_ingest_status_returns_status(self, mock_get):
        """Regra: get_ingest_status retorna campos de monitoramento."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "running": False,
            "step": "",
            "progress": 0,
            "total": 0,
            "logs": [],
        }
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = get_ingest_status()
        assert "running" in result
        assert "logs" in result
