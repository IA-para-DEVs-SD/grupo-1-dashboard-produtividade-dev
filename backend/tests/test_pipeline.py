"""Tests for RAG pipeline."""
import json
from unittest.mock import MagicMock, patch

import pytest

from src.rag.pipeline import RAGPipeline


class TestRAGPipeline:
    @patch("src.rag.pipeline.EmbeddingService")
    @patch("src.rag.pipeline.VectorStore")
    @patch("src.rag.pipeline.LLMClient")
    def test_build_prompt(self, mock_llm, mock_store, mock_embed):
        pipeline = RAGPipeline()
        chunks = ["Commit abc: fix bug", "PR #1: add feature"]
        prompt = pipeline._build_prompt(chunks, "O que fiz hoje?")
        assert "Commit abc: fix bug" in prompt
        assert "PR #1: add feature" in prompt
        assert "O que fiz hoje?" in prompt

    @patch("src.rag.pipeline.EmbeddingService")
    @patch("src.rag.pipeline.VectorStore")
    @patch("src.rag.pipeline.LLMClient")
    @pytest.mark.asyncio
    async def test_query_no_chunks(self, mock_llm, mock_store, mock_embed):
        mock_embed_instance = MagicMock()
        mock_embed_instance.embed.return_value = [0.1] * 384
        mock_embed.return_value = mock_embed_instance

        mock_store_instance = MagicMock()
        mock_store_instance.query.return_value = []
        mock_store.return_value = mock_store_instance

        pipeline = RAGPipeline()
        result = await pipeline.query("teste")

        assert "Sem dados suficientes" in result.summary
        assert "ingestão" in result.recommendation.lower()

    @patch("src.rag.pipeline.EmbeddingService")
    @patch("src.rag.pipeline.VectorStore")
    @patch("src.rag.pipeline.LLMClient")
    @pytest.mark.asyncio
    async def test_query_with_valid_json(self, mock_llm, mock_store, mock_embed):
        mock_embed_instance = MagicMock()
        mock_embed_instance.embed.return_value = [0.1] * 384
        mock_embed.return_value = mock_embed_instance

        mock_store_instance = MagicMock()
        mock_store_instance.query.return_value = [
            {"document": "Commit abc: fix bug", "distance": 0.1, "metadata": {}}
        ]
        mock_store.return_value = mock_store_instance

        mock_llm_instance = MagicMock()
        mock_llm_instance.complete.return_value = json.dumps({
            "summary": "Você corrigiu um bug",
            "evidence": "Commit abc",
            "recommendation": "Continue assim",
        })
        mock_llm.return_value = mock_llm_instance

        pipeline = RAGPipeline()
        result = await pipeline.query("O que fiz?")

        assert result.summary == "Você corrigiu um bug"
        assert result.evidence == "Commit abc"
        assert result.recommendation == "Continue assim"

    @patch("src.rag.pipeline.EmbeddingService")
    @patch("src.rag.pipeline.VectorStore")
    @patch("src.rag.pipeline.LLMClient")
    @pytest.mark.asyncio
    async def test_query_with_list_evidence(self, mock_llm, mock_store, mock_embed):
        mock_embed_instance = MagicMock()
        mock_embed_instance.embed.return_value = [0.1] * 384
        mock_embed.return_value = mock_embed_instance

        mock_store_instance = MagicMock()
        mock_store_instance.query.return_value = [
            {"document": "Commit abc", "distance": 0.1, "metadata": {}}
        ]
        mock_store.return_value = mock_store_instance

        mock_llm_instance = MagicMock()
        mock_llm_instance.complete.return_value = json.dumps({
            "summary": "Resumo",
            "evidence": ["item1", "item2"],
            "recommendation": {"tip": "dica"},
        })
        mock_llm.return_value = mock_llm_instance

        pipeline = RAGPipeline()
        result = await pipeline.query("teste")

        assert "item1" in result.evidence
        assert "item2" in result.evidence
        assert "dica" in result.recommendation

    @patch("src.rag.pipeline.EmbeddingService")
    @patch("src.rag.pipeline.VectorStore")
    @patch("src.rag.pipeline.LLMClient")
    @pytest.mark.asyncio
    async def test_query_invalid_json(self, mock_llm, mock_store, mock_embed):
        mock_embed_instance = MagicMock()
        mock_embed_instance.embed.return_value = [0.1] * 384
        mock_embed.return_value = mock_embed_instance

        mock_store_instance = MagicMock()
        mock_store_instance.query.return_value = [
            {"document": "Commit abc", "distance": 0.1, "metadata": {}}
        ]
        mock_store.return_value = mock_store_instance

        mock_llm_instance = MagicMock()
        mock_llm_instance.complete.return_value = "Resposta em texto livre"
        mock_llm.return_value = mock_llm_instance

        pipeline = RAGPipeline()
        result = await pipeline.query("teste")

        assert result.summary == "Resposta em texto livre"
        assert result.evidence == ""
