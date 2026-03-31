"""Testes unitários para o serviço de ingestão.

Valida: status tracking, retorno 0 sem token, fluxo completo com mocks,
e que o scheduler é configurado com intervalo de 12h.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.ingestion import (
    IngestionStatus,
    get_ingestion_status,
    run_ingestion,
    start_scheduler,
)


class TestIngestionStatus:
    def test_initial_status_not_running(self):
        """Regra: status inicial indica que não há ingestão em andamento."""
        status = IngestionStatus()
        assert status.running is False
        assert status.error is None
        assert status.logs == []

    def test_get_ingestion_status_returns_dict(self):
        """Regra: endpoint /ingest/status retorna dict com campos esperados."""
        result = get_ingestion_status()
        assert "running" in result
        assert "step" in result
        assert "progress" in result
        assert "total" in result
        assert "logs" in result


class TestRunIngestion:
    @pytest.mark.asyncio
    async def test_returns_zero_without_github_token(self):
        """Regra: sem GITHUB_TOKEN configurado, ingestão retorna 0 chunks."""
        with patch("src.services.ingestion.settings") as mock_settings:
            mock_settings.github_token = ""
            mock_settings.ingestion_days_back = 90
            result = await run_ingestion()
        assert result == 0

    @pytest.mark.asyncio
    async def test_full_ingestion_flow_with_mocks(self):
        """Regra: ingestão coleta dados, gera embeddings e salva no ChromaDB."""
        mock_collector = MagicMock()
        mock_collector.fetch_commits = AsyncMock(return_value=[
            MagicMock(
                to_chunk=lambda: "commit chunk",
                to_metadata=lambda: {"type": "commit", "date": "2026-03-20"},
            )
        ])
        mock_collector.fetch_pull_requests = AsyncMock(return_value=[])
        mock_collector.fetch_issues = AsyncMock(return_value=[])

        mock_embedder = MagicMock()
        mock_embedder.embed_batch.return_value = [[0.1] * 384]

        mock_store = MagicMock()

        with (
            patch("src.services.ingestion.settings") as mock_settings,
            patch(
                "src.services.ingestion.GitHubCollector",
                return_value=mock_collector,
            ),
            patch(
                "src.services.ingestion.EmbeddingService",
                return_value=mock_embedder,
            ),
            patch("src.services.ingestion.VectorStore", return_value=mock_store),
        ):
            mock_settings.github_token = "ghp_test123"
            mock_settings.ingestion_days_back = 90
            result = await run_ingestion()

        assert result == 1
        mock_store.upsert.assert_called_once()
        call_kwargs = mock_store.upsert.call_args
        assert len(call_kwargs.kwargs["documents"]) == 1


class TestScheduler:
    def test_scheduler_starts_with_12h_interval(self):
        """Regra: scheduler de ingestão roda a cada 12 horas."""
        with patch("src.services.ingestion.BackgroundScheduler") as mock_sched_cls:
            mock_sched = MagicMock()
            mock_sched_cls.return_value = mock_sched
            start_scheduler()
            mock_sched.add_job.assert_called_once()
            call_args = mock_sched.add_job.call_args
            assert call_args[1].get("hours") == 12
            mock_sched.start.assert_called_once()
