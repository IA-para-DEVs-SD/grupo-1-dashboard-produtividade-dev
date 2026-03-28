from pydantic import BaseModel


class Insight(BaseModel):
    summary: str
    evidence: str
    recommendation: str
    sources: list[str] = []
