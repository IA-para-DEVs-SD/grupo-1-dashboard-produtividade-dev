"""Tests for GitHub models."""
from datetime import datetime

from src.github.models import Commit, Issue, PullRequest


class TestCommit:
    def test_to_chunk_basic(self):
        commit = Commit(
            sha="abc1234567890",
            message="feat: add login",
            author="sergio",
            date=datetime(2026, 3, 20, 10, 30),
            additions=50,
            deletions=10,
            repository="user/repo",
        )
        chunk = commit.to_chunk()
        assert "abc1234" in chunk
        assert "feat: add login" in chunk
        assert "50 adições" in chunk
        assert "10 deleções" in chunk
        assert "sergio" in chunk
        assert "user/repo" in chunk
        assert "2026-03-20" in chunk

    def test_to_metadata(self):
        commit = Commit(
            sha="abc123",
            message="fix: bug",
            author="dev",
            date=datetime(2026, 3, 15, 8, 0),
            repository="org/project",
        )
        meta = commit.to_metadata()
        assert meta["type"] == "commit"
        assert meta["author"] == "dev"
        assert meta["repository"] == "org/project"
        assert "2026-03-15" in meta["date"]


class TestPullRequest:
    def test_to_chunk_open(self):
        pr = PullRequest(
            title="Add feature X",
            state="OPEN",
            created_at=datetime(2026, 3, 18),
            repository="user/repo",
            number=42,
        )
        chunk = pr.to_chunk()
        assert "PR #42" in chunk
        assert "Add feature X" in chunk
        assert "OPEN" in chunk
        assert "user/repo" in chunk

    def test_to_chunk_merged(self):
        pr = PullRequest(
            title="Fix bug",
            state="MERGED",
            created_at=datetime(2026, 3, 10),
            merged_at=datetime(2026, 3, 12),
            repository="org/app",
            number=100,
        )
        chunk = pr.to_chunk()
        assert "merged em 2026-03-12" in chunk

    def test_to_metadata(self):
        pr = PullRequest(
            title="Test",
            state="CLOSED",
            created_at=datetime(2026, 3, 5),
            repository="test/repo",
            number=1,
        )
        meta = pr.to_metadata()
        assert meta["type"] == "pr"
        assert meta["repository"] == "test/repo"


class TestIssue:
    def test_to_chunk_open(self):
        issue = Issue(
            title="Bug report",
            state="OPEN",
            labels=["bug", "urgent"],
            created_at=datetime(2026, 3, 1),
            repository="user/project",
            number=55,
        )
        chunk = issue.to_chunk()
        assert "Issue #55" in chunk
        assert "Bug report" in chunk
        assert "bug" in chunk
        assert "urgent" in chunk

    def test_to_chunk_closed(self):
        issue = Issue(
            title="Feature request",
            state="CLOSED",
            labels=[],
            created_at=datetime(2026, 2, 20),
            closed_at=datetime(2026, 3, 1),
            repository="org/lib",
            number=10,
        )
        chunk = issue.to_chunk()
        assert "fechada em 2026-03-01" in chunk

    def test_to_metadata(self):
        issue = Issue(
            title="Test",
            state="OPEN",
            created_at=datetime(2026, 3, 10),
            repository="test/repo",
            number=1,
        )
        meta = issue.to_metadata()
        assert meta["type"] == "issue"
        assert meta["repository"] == "test/repo"
