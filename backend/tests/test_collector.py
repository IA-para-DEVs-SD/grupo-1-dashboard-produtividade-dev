"""Testes unitários para GitHubCollector.

Valida: construção de headers com token, check_connection,
parsing de commits/PRs/issues a partir de respostas GraphQL mockadas,
e tratamento de erros de rede.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.github.collector import GitHubCollector


class TestCollectorInit:
    def test_sets_bearer_token_in_headers(self):
        """Regra: autenticação via GitHub PAT no header Authorization."""
        collector = GitHubCollector(token="ghp_test123", days_back=30)
        assert collector.headers["Authorization"] == "bearer ghp_test123"

    def test_days_back_configurable(self):
        """Regra: período de coleta é configurável (default 90 dias)."""
        collector = GitHubCollector(token="t", days_back=60)
        assert collector.days_back == 60


class TestCheckConnection:
    @pytest.mark.asyncio
    async def test_returns_connected_true_on_success(self):
        """Regra: /github/status retorna connected=True com login."""
        collector = GitHubCollector(token="ghp_test", days_back=90)
        mock_response = {"viewer": {"login": "testuser"}}
        with patch.object(
            collector,
            "_query",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await collector.check_connection()
        assert result["connected"] is True
        assert result["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_returns_connected_false_on_error(self):
        """Regra: falha de rede retorna connected=False com mensagem de erro."""
        collector = GitHubCollector(token="ghp_bad", days_back=90)
        with patch.object(
            collector,
            "_query",
            new_callable=AsyncMock,
            side_effect=Exception("timeout"),
        ):
            result = await collector.check_connection()
        assert result["connected"] is False
        assert "timeout" in result["error"]


class TestFetchCommits:
    @pytest.mark.asyncio
    async def test_parses_commits_from_graphql_response(self):
        """Regra: commits são extraídos com sha, message, author, date, repo."""
        collector = GitHubCollector(token="ghp_test", days_back=90)
        graphql_data = {
            "viewer": {
                "repositories": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": [
                        {
                            "nameWithOwner": "user/repo",
                            "defaultBranchRef": {
                                "target": {
                                    "history": {
                                        "pageInfo": {
                                            "hasNextPage": False,
                                            "endCursor": None,
                                        },
                                        "nodes": [
                                            {
                                                "oid": "abc1234567890",
                                                "message": "feat: add login",
                                                "author": {"name": "dev"},
                                                "committedDate": "2026-03-20T10:30:00Z",
                                                "additions": 50,
                                                "deletions": 10,
                                            }
                                        ],
                                    }
                                }
                            },
                        }
                    ],
                }
            }
        }
        with patch.object(
            collector, "_query", new_callable=AsyncMock, return_value=graphql_data
        ):
            commits = await collector.fetch_commits()
        assert len(commits) == 1
        assert commits[0].sha == "abc1234567890"
        assert commits[0].author == "dev"
        assert commits[0].repository == "user/repo"
        assert commits[0].additions == 50

    @pytest.mark.asyncio
    async def test_skips_repos_without_default_branch(self):
        """Regra: repos sem defaultBranchRef são ignorados sem erro."""
        collector = GitHubCollector(token="ghp_test", days_back=90)
        graphql_data = {
            "viewer": {
                "repositories": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": [
                        {
                            "nameWithOwner": "user/empty",
                            "defaultBranchRef": None,
                        }
                    ],
                }
            }
        }
        with patch.object(
            collector, "_query", new_callable=AsyncMock, return_value=graphql_data
        ):
            commits = await collector.fetch_commits()
        assert commits == []


class TestFetchAllChunks:
    @pytest.mark.asyncio
    async def test_aggregates_commits_prs_issues_into_chunks(
        self,
    ):
        """Regra: fetch_all_chunks retorna tuplas
        (chunk_text, metadata) de todos os tipos."""
        collector = GitHubCollector(token="ghp_test", days_back=90)
        with (
            patch.object(
                collector,
                "fetch_commits",
                new_callable=AsyncMock,
                return_value=[
                    MagicMock(
                        to_chunk=lambda: "commit chunk",
                        to_metadata=lambda: {"type": "commit"},
                        date=datetime(2026, 3, 20, tzinfo=timezone.utc),
                        repository="r",
                        author="a",
                    )
                ],
            ),
            patch.object(
                collector,
                "fetch_pull_requests",
                new_callable=AsyncMock,
                return_value=[
                    MagicMock(
                        to_chunk=lambda: "pr chunk",
                        to_metadata=lambda: {"type": "pr"},
                        created_at=datetime(2026, 3, 20, tzinfo=timezone.utc),
                        repository="r",
                    )
                ],
            ),
            patch.object(
                collector,
                "fetch_issues",
                new_callable=AsyncMock,
                return_value=[
                    MagicMock(
                        to_chunk=lambda: "issue chunk",
                        to_metadata=lambda: {"type": "issue"},
                        created_at=datetime(2026, 3, 20, tzinfo=timezone.utc),
                        repository="r",
                    )
                ],
            ),
        ):
            chunks = await collector.fetch_all_chunks()
        assert len(chunks) == 3
        types = {c[1]["type"] for c in chunks}
        assert types == {"commit", "pr", "issue"}

    @pytest.mark.asyncio
    async def test_continues_on_partial_failure(self):
        """Regra: se commits falhar, PRs e issues ainda são coletados."""
        collector = GitHubCollector(token="ghp_test", days_back=90)
        with (
            patch.object(
                collector,
                "fetch_commits",
                new_callable=AsyncMock,
                side_effect=Exception("API error"),
            ),
            patch.object(
                collector,
                "fetch_pull_requests",
                new_callable=AsyncMock,
                return_value=[],
            ),
            patch.object(
                collector, "fetch_issues", new_callable=AsyncMock, return_value=[]
            ),
        ):
            chunks = await collector.fetch_all_chunks()
        assert chunks == []  # Nenhum dado, mas sem exceção
