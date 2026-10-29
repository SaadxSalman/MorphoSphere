"""
LangGraph Workflow Orchestration.

Orchestrates the end-to-end MorphoSphere pipeline using LangGraph:
  Ingestion -> Retrieval -> Agentic Validation -> Generation
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.agent.validation import validation_agent
from app.config import settings
from app.database.neo4j_client import neo4j_client
from app.database.qdrant_client import qdrant_client
from app.ingestion.pipeline import ingestion_pipeline
from app.models.document import IngestedDocument
from app.models.query import QueryResponse
from app.retrieval.hybrid import hybrid_retrieval_engine

logger = logging.getLogger(__name__)


class MorphoSphereWorkflow:
    """
    LangGraph-based workflow that connects ingestion, retrieval,
    and agentic correction into a single orchestrated pipeline.
    """

    def __init__(self) -> None:
        self.ingestion = ingestion_pipeline

    def query(
        self,
        query_text: str,
        intent: Optional[str] = None,
        top_k: int = 10,
        enable_agentic: bool = True,
    ) -> QueryResponse:
        """
        Execute the full query pipeline:

        1. Hybrid retrieval (semantic + topological + lexical + RRF)
        2. Agentic self-correction (recursive expansion)
        3. Answer generation (via LLM)
        """
        import time

        start_time = time.time()

        query_intent = None
        if intent:
            from app.models.query import QueryIntent
            try:
                query_intent = QueryIntent(intent)
            except ValueError:
                query_intent = None

        retrieval_output = self.retrieval.retrieve(
            query_text, intent=query_intent, top_k=top_k
        )
        results = retrieval_output["fused_results"]
        graph_context = retrieval_output["graph_context"]
        detected_intent = retrieval_output["intent"]

        agentic_passes = 0
        if enable_agentic and settings.feature_agentic_loop:
            correction_output = self.agent.validate_and_correct(
                query_text, results, graph_context
            )
            results = correction_output["corrected_results"]

    def _generate_answer(
        self,
        query: str,
        results: List[Any],
        graph_context: List[Any],
        intent: Any,
    ) -> tuple:
        """
        Generate a natural language answer from retrieval results.

        Uses the LLM if available; otherwise falls back to an extractive
        summary of the top results.
        """
        context_parts = []
        for r in results[:5]:
            content = r.content if hasattr(r, "content") else str(r)
            context_parts.append(f"[Source] {content[:500]}")

        context = "\n".join(context_parts) if context_parts else "No relevant context found."

        try:
            import httpx

            llm_url = f"{settings.llm_base_url}/api/generate"
            prompt = f"""You are MorphoSphere, an advanced structural pattern recognition engine.
            Answer the user's query using only the provided context from the codebase graph.

            Query: {query}
            Intent: {intent}
            Context:
            {context}

            Provide a detailed, technically accurate answer referencing specific code elements,
            file paths, and line numbers where available.
            """
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(
                    llm_url,
                    json={
                        "model": settings.llm_model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": settings.llm_temperature,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data.get("response", "")
                    return answer, 0.85
        except Exception:  # noqa: BLE001
            logger.debug("LLM unavailable, using extractive fallback")

        answer = (
            f"Based on structural pattern analysis of your codebase, here are the "
            f"most relevant findings for: '{query}'\n\n"
        )
        for i, r in enumerate(results[:5], 1):
            content = r.content if hasattr(r, "content") else str(r)
            answer += f"{i}. {content[:300]}...\n"

        return answer, 0.65

    def health_check(self) -> Dict[str, Any]:
        """Check health of all connected services."""
        return {
            "neo4j": neo4j_client.is_connected,
            "qdrant": qdrant_client.is_connected,
            "llm": settings.llm_provider,
            "status": "healthy" if (neo4j_client.is_connected or qdrant_client.is_connected) else "degraded",
        }


# Singleton instance
morpho_workflow = MorphoSphereWorkflow()
            graph_context = correction_output["graph_context"]
            agentic_passes = correction_output["passes"]

        answer, confidence = self._generate_answer(
            query_text, results, graph_context, detected_intent
        )

        processing_time = (time.time() - start_time) * 1000

        return QueryResponse(
            query=query_text,
            intent=detected_intent,
            results=results,
            generated_answer=answer,
            confidence=confidence,
            agentic_passes=agentic_passes,
            graph_context=graph_context,
            processing_time_ms=processing_time,
        )
        self.retrieval = hybrid_retrieval_engine
        self.agent = validation_agent

    def ingest_and_index(self, file_path: str, content: Optional[str] = None) -> IngestedDocument:
        """
        Ingest a file and index it in both Neo4j and Qdrant.
        """
        logger.info("Starting ingestion for: %s", file_path)
        doc = self.ingestion.ingest_file(file_path, content)
        logger.info("Ingestion complete: %s (%d nodes)", doc.filename, doc.node_count)
        return doc