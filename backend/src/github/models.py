from datetime import datetime

from pydantic import BaseModel


class Commit(BaseModel):
    sha: str
    message: str
    author: str
    date: datetime
    additions: int = 0
    deletions: int = 0
    repository: str = ""

    def to_chunk(self) -> str:
        return (
            f"Commit {self.sha[:7]}: {self.message.strip()} — "
            f"{self.additions} adições, {self.deletions} deleções — "
            f"autor: {self.author} — repo: {self.repository} — {self.date:%Y-%m-%d}"
        )

    def to_metadata(self) -> dict:
        return {
            "type": "commit",
            "date": self.date.isoformat(),
            "repository": self.repository,
            "author": self.author,
        }


class PullRequest(BaseModel):
    title: str
    state: str
    created_at: datetime
    merged_at: datetime | None = None
    repository: str = ""
    number: int = 0

    def to_chunk(self) -> str:
        merged = f" — merged em {self.merged_at:%Y-%m-%d}" if self.merged_at else ""
        return (
            f"PR #{self.number}: {self.title} — estado: {self.state}"
            f" — repo: {self.repository} — criado em {self.created_at:%Y-%m-%d}{merged}"
        )

    def to_metadata(self) -> dict:
        return {
            "type": "pr",
            "date": self.created_at.isoformat(),
            "repository": self.repository,
            "author": "",
        }


class Issue(BaseModel):
    title: str
    state: str
    labels: list[str] = []
    created_at: datetime
    closed_at: datetime | None = None
    repository: str = ""
    number: int = 0

    def to_chunk(self) -> str:
        labels = f" — labels: {', '.join(self.labels)}" if self.labels else ""
        closed = f" — fechada em {self.closed_at:%Y-%m-%d}" if self.closed_at else ""
        return (
            f"Issue #{self.number}: {self.title} — estado: {self.state}"
            f" — repo: {self.repository} — criada em {self.created_at:%Y-%m-%d}{labels}{closed}"
        )

    def to_metadata(self) -> dict:
        return {
            "type": "issue",
            "date": self.created_at.isoformat(),
            "repository": self.repository,
            "author": "",
        }
