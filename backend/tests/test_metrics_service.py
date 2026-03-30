"""Testes unitários para o serviço de métricas.

Valida: cálculo de KPIs, cache em memória, filtro por data,
tempo médio de merge, hot repos, e retorno de erro sem token.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.metrics import MetricsService, _cache


@pytest.fixture(autouse=True)
def _clear_cache():
    """Limpa cache entre testes."""
    _cache.clear()
    yield
    _cache.clear()


class TestMetricsCalculate:
    @pytest.mark.asyncio
    async def test_returns_error_without_github_token(self):
        """Regra: sem GITHUB_TOKEN, retorna erro descritivo."""
        with patch("src.services.metrics.settings") as mock_settings:
            mock_settings.github_token = ""
            svc = MetricsService()
            result = await svc.calculate()
        assert "error" in result
        assert "GITHUB_TOKEN" in result["error"]

    @pytest.mark.asyncio
    async def test_calculates_kpis_from_github_data(self):
        """Regra: KPIs incluem total_commits, total_prs, prs_merged, hot_repos."""
        mock_commits = [
            MagicMock(
                date=datetime(2026, 3, 20, tzinfo=timezone.utc),
                repository="user/repo-a",
            ),
            MagicMock(
                date=datetime(2026, 3, 21, tzinfo=timezone.utc),
                repository="user/repo-a",
            ),
            MagicMock(
                date=datetime(2026, 3, 22, tzinfo=timezone.utc),
                repository="user/repo-b",
            ),
        ]
        mock_prs = [
            MagicMock(
                created_at=datetime(2026, 3, 18, tzinfo=timezone.utc),
                merged_at=datetime(2026, 3, 20, tzinfo=timezone.utc),
                state="MERGED",
            ),
        ]
        mock_issues = [
            MagicMock(
                created_at=datetime(2026, 3, 15, tzinfo=timezone.utc),
                closed_at=datetime(2026, 3, 18, tzinfo=timezone.utc),
                state="CLOSED",
            ),
            MagicMock(
                created_at=datetime(2026, 3, 16, tzinfo=timezone.utc),
                closed_at=None,
                state="OPEN",
            ),
        ]

        mock_collector = MagicMock()
        mock_collector.fetch_commits = AsyncMock(return_value=mock_commits)
        mock_collector.fetch_pull_requests = AsyncMock(return_value=mock_prs)
        mock_collector.fetch_issues = AsyncMock(return_value=mock_issues)

        with (
            patch("src.services.metrics.settings") as mock_settings,
            patch("src.services.metrics.GitHubCollector", return_value=mock_collector),
        ):
            mock_settings.github_token = "ghp_test"
            mock_settings.ingestion_days_back = 90
            svc = MetricsService()
            result = await svc.calculate()

        assert result["total_commits"] == 3
        assert result["total_prs"] == 1
        assert result["total_issues"] == 2
        assert result["prs_merged"] == 1
        assert result["issues_fechadas"] == 1
        assert result["tempo_medio_merge_horas"] > 0
        assert len(result["hot_repos"]) > 0
        assert result["hot_repos"][0]["repo"] == "user/repo-a"

    @pytest.mark.asyncio
    async def test_cache_returns_same_result(self):
        """Regra: cache em memória evita chamadas repetidas ao GitHub."""
        mock_collector = MagicMock()
        mock_collector.fetch_commits = AsyncMock(return_value=[])
        mock_collector.fetch_pull_requests = AsyncMock(return_value=[])
        mock_collector.fetch_issues = AsyncMock(return_value=[])

        with (
            patch("src.services.metrics.settings") as mock_settings,
            patch("src.services.metrics.GitHubCollector", return_value=mock_collector),
        ):
            mock_settings.github_token = "ghp_test"
            mock_settings.ingestion_days_back = 90
            svc = MetricsService()
            result1 = await svc.calculate()
            result2 = await svc.calculate()

        assert result1 == result2
        # Collector só foi chamado 1 vez (segunda veio do cache)
        assert mock_collector.fetch_commits.call_count == 1
