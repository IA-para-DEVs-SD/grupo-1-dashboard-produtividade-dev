import json

from src.rag.embeddings import EmbeddingService
from src.rag.llm_client import LLMClient
from src.rag.models import Insight
from src.rag.vector_store import VectorStore

PROMPT_TEMPLATE = """Você é um assistente de produtividade para desenvolvedores.
Com base nos seguintes dados reais do GitHub do usuário:

{chunks}

Responda à pergunta: {query}

Responda APENAS em JSON válido com este formato (sem markdown, sem ```):
{{"summary": "resposta curta", "evidence": "dados", "recommendation": "sugestão"}}
"""


class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()
        self.llm = LLMClient()

    def _build_prompt(self, chunks: list[str], query: str) -> str:
        chunks_text = "\n".join(f"- {c}" for c in chunks)
        return PROMPT_TEMPLATE.format(chunks=chunks_text, query=query)

    async def query(self, user_input: str) -> Insight:
        query_vec = self.embedder.embed(user_input)
        results = self.store.query(query_vec, top_k=5)
        chunks = [r["document"] for r in results]

        if not chunks:
            return Insight(
                summary="Sem dados suficientes para responder.",
                evidence="Nenhum chunk encontrado no ChromaDB.",
                recommendation="Execute a ingestão de dados primeiro.",
            )

        prompt = self._build_prompt(chunks, user_input)
        raw = self.llm.complete(prompt)

        try:
            parsed = json.loads(raw)
            summary = parsed.get("summary", raw)
            evidence = parsed.get("evidence", "")
            recommendation = parsed.get("recommendation", "")
            
            # Format non-string values nicely
            if isinstance(evidence, list):
                evidence = "\n• " + "\n• ".join(str(e) for e in evidence)
            elif not isinstance(evidence, str):
                evidence = str(evidence)
                
            if isinstance(recommendation, (list, set)):
                recommendation = "\n• " + "\n• ".join(str(r) for r in recommendation)
            elif isinstance(recommendation, dict):
                recommendation = "\n• " + "\n• ".join(str(v) for v in recommendation.values())
            elif not isinstance(recommendation, str):
                recommendation = str(recommendation)
            
            return Insight(
                summary=summary if isinstance(summary, str) else str(summary),
                evidence=evidence,
                recommendation=recommendation,
                sources=chunks,
            )
        except json.JSONDecodeError:
            return Insight(
                summary=raw,
                evidence="",
                recommendation="",
                sources=chunks,
            )
