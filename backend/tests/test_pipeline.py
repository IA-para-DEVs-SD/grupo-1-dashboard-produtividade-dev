"""Testes unitários para o RAG pipeline.

Valida: construção de prompt, query sem chunks, query com JSON válido,
query com JSON inválido, formatação de evidence/recommendation não-string.
"""

import json
from unittest.mock import MagicMock

import pytest

from src.rag.pipeline import RAGPipeline


@pytest.fixture()
def pipeline():
    """Cria RAGPipeline com todas as dependências mockadas."""
    p = RAGPipeline.__new__(RAGPipeline)
    p.embedder = MagicMock()
    p.embedder.embed.return_value = [0.1] * 384
    p.store = MagicMock()
    p.llm = MagicMock()
    return p


class TestBuildPrompt:
    def test_prompt_contains_chunks_and_query(self, pipeline):
        chunks = ["Commit abc: fix bug", "PR #1: add feature"]
        prompt = pipeline._build_prompt(chunks, "O que fiz hoje?")
        assert "Commit abc: fix bug" in prompt
        assert "PR #1: add feature" in prompt
        assert "O que fiz hoje?" in prompt

    def test_prompt_uses_template_format(self, pipeline):
        prompt = pipeline._build_prompt(["chunk1"], "pergunta")
        assert "JSON" in prompt
        assert "summary" in prompt


class TestQueryNoChunks:
    @pytest.mark.asyncio
    async def test_returns_no_data_message(self, pipeline):
        pipeline.store.query.return_value = []
        result = await pipeline.query("teste")
        assert "Sem dados suficientes" in result.summary
        assert "ingestão" in result.recommendation.lower()


class TestQueryValidJson:
    @pytest.mark.asyncio
    async def test_parses_json_response(self, pipeline):
        pipeline.store.query.return_value = [
            {"document": "Commit abc: fix bug", "distance": 0.1, "metadata": {}}
        ]
        pipeline.llm.complete.return_value = json.dumps({
            "summary": "Você corrigiu um bug",
            "evidence": "Commit abc",
            "recommendation": "Continue assim",
        })
        result = await pipeline.query("O que fiz?")
        assert result.summary == "Você corrigiu um bug"
        assert result.evidence == "Commit abc"
        assert result.recommendation == "Continue assim"


class TestQueryListEvidence:
    @pytest.mark.asyncio
    async def test_formats_list_evidence(self, pipeline):
        pipeline.store.query.return_value = [
            {"document": "Commit abc", "distance": 0.1, "metadata": {}}
        ]
        pipeline.llm.complete.return_value = json.dumps({
            "summary": "Resumo",
            "evidence": ["item1", "item2"],
            "recommendation": {"tip": "dica"},
        })
        result = await pipeline.query("teste")
        assert "item1" in result.evidence
        assert "item2" in result.evidence
        assert "dica" in result.recommendation


class TestQueryInvalidJson:
    @pytest.mark.asyncio
    async def test_falls_back_to_raw_text(self, pipeline):
        pipeline.store.query.return_value = [
            {"document": "Commit abc", "distance": 0.1, "metadata": {}}
        ]
        pipeline.llm.complete.return_value = "Resposta em texto livre"
        result = await pipeline.query("teste")
        assert result.summary == "Resposta em texto livre"
        assert result.evidence == ""
