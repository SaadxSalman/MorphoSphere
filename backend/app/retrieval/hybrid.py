"""
Hybrid Pattern-Semantic Retrieval Engine.

Combines BM25 lexical matching, dense semantic vector similarity,
and structural graph retrieval to fetch the most accurate context
window for complex technical queries.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.config import settings
from app.database.neo4j_client import neo4j_client
from app.database.qdrant_client import qdrant_client
from app.models.document import DocumentNode, RetrievalResult
from app.models.query import HybridSearchRequest, QueryIntent
from app.retrieval.intent import intent_classifier
from app.retrieval.rrf import reciprocal_rank_fusion, weighted_score_fusion
from app.vectorization.semantic import semantic_embedder
from app.vectorization.topological import topological_embedder

logger = logging.getLogger(__name__)


class HybridRetrievalEngine:
    """
    Multi-stage retrieval engine:

    1. Intent-to-pattern translation
    2. Parallel semantic, topological, and lexical search

    def retrieve(self, query: str, intent: Optional[QueryIntent] = None, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute the full hybrid retrieval pipeline.

        Returns a dict with:
          - intent: detected/classified intent
          - semantic_results: raw semantic hits
          - topological_results: raw topological hits
          - lexical_results: raw lexical hits
          - fused_results: RRF-fused results
          - graph_context: expanded graph neighborhood
        """
        top_k = top_k or self.top_k

        # Step 1: Intent classification
        if intent is None:
            classification = intent_classifier.classify(query)
            detected_intent = classification.intent
            logger.info("Query intent: %s (confidence: %.2f)", detected_intent, classification.confidence)
        else:
            detected_intent = intent
            classification = None

        # Step 2: Generate query vector for semantic search
        query_vector = semantic_embedder.embed_text(query)

        # Step 3: Parallel searches
        semantic_results = qdrant_client.search_semantic(
            query_vector, limit=top_k
        ) if qdrant_client.is_connected else []

        topo_vector = topological_embedder.embed_graph([], [])
        topo_query_vector = [0.0] * len(topo_vector[0]) if topo_vector else [0.0] * 768
        topological_results = qdrant_client.search_topological(
            topo_query_vector, limit=top_k
        ) if qdrant_client.is_connected else []

        # Step 4: Lexical search (BM25-style via Neo4j or simple text matching)
        lexical_results = self._lexical_search(query, top_k)

        # Step 5: Fuse results using RRF
        ranked_lists = [semantic_results, topological_results, lexical_results]
        weights = [self.semantic_weight, self.topological_weight, self.lexical_weight]
        fused_results = reciprocal_rank_fusion(ranked_lists, k=self.rrf_k, weights=weights)
    3. Reciprocal Rank Fusion (RRF)

        # Step 6: Enrich fused results with node details
        enriched_results: List[RetrievalResult] = []
        for item in fused_results[:top_k]:
            node_id = item.get("id")
            node = self._get_node_by_id(node_id) if node_id else None
            enriched_results.append(
                RetrievalResult(
                    document_id=UUID(item.get("payload", {}).get("document_id", "00000000-0000-0000-0000-000000000000")) if item.get("payload") else uuid4(),
                    node_id=UUID(node_id) if node_id else None,
                    content=node.content if node else item.get("payload", {}).get("content", ""),
                    semantic_score=item.get("semantic_score", 0.0),
                    topological_score=item.get("topological_score", 0.0),
                    lexical_score=item.get("lexical_score", 0.0),
                    fused_score=item.get("rrf_score", item.get("fused_score", 0.0)),
                    graph_neighbors=[],
                    metadata=item.get("payload", {}),
                )
            )

        # Step 7: Graph context expansion
        graph_context: List[DocumentNode] = []
        if neo4j_client.is_connected and enriched_results:
            for result in enriched_results[:5]:
                if result.node_id:
                    neighbors = neo4j_client.get_node_neighbors(result.node_id, depth=1)
                    for nb in neighbors:
                        graph_context.append(
                            DocumentNode(
                                id=UUID(nb.get("id", str(uuid4()))),
                                document_id=uuid4(),
                                node_type=nb.get("node_type", "unknown"),
                                name=nb.get("name", "unknown"),
                                language=__import__("app.models.document", fromlist=["Language"]).Language.UNKNOWN,
                                file_path=nb.get("file_path", ""),
                                start_line=nb.get("start_line", 0),
                                end_line=nb.get("end_line", 0),
                                content=nb.get("content", ""),
                                metadata={},
                            )
                        )

        return {
            "intent": detected_intent,
            "classification": classification,
            "semantic_results": semantic_results,
            "topological_results": topological_results,
            "lexical_results": lexical_results,
            "fused_results": enriched_results,
            "graph_context": graph_context,
        }

    def _lexical_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Simple lexical (BM25-style) search using keyword matching.

        In production this would integrate with a proper BM25 index.
        """
        results: List[Dict[str, Any]] = []
        query_terms = set(query.lower().split())

        if neo4j_client.is_connected:
            records = neo4j_client.run_cypher(
                """
                MATCH (n:Node)
                WHERE any(term IN $terms WHERE toLower(n.content) CONTAINS term)
                RETURN n.id AS id, n.name AS name, n.content AS content,
                       n.file_path AS file_path, n.node_type AS node_type
                LIMIT $limit
                """,
                {"terms": list(query_terms), "limit": top_k},
            )
            for rec in records:
                results.append({
                    "id": rec.get("id", ""),
                    "name": rec.get("name", ""),
                    "content": rec.get("content", ""),
                    "file_path": rec.get("file_path", ""),
                    "node_type": rec.get("node_type", ""),
                    "lexical_score": 1.0,
                })

        return results

    def _get_node_by_id(self, node_id: str) -> Optional[DocumentNode]:
        """Fetch a node by ID from Neo4j."""
        if not neo4j_client.is_connected:
            return None
        records = neo4j_client.run_cypher(
            "MATCH (n:Node {id: $id}) RETURN n LIMIT 1",
            {"id": node_id},
        )
        if records:
            rec = records[0].get("n", {})
            return DocumentNode(
                id=UUID(node_id),
                document_id=uuid4(),
                node_type=rec.get("node_type", "unknown"),
                name=rec.get("name", "unknown"),
                language=__import__("app.models.document", fromlist=["Language"]).Language.UNKNOWN,
                file_path=rec.get("file_path", ""),
                start_line=rec.get("start_line", 0),
                end_line=rec.get("end_line", 0),
                content=rec.get("content", ""),
                metadata={},
            )
        return None
    4. Optional recursive graph expansion
    """

    def __init__(self) -> None:
        self.top_k = settings.retrieval_top_k
        self.semantic_weight = settings.retrieval_semantic_weight
        self.topological_weight = settings.retrieval_topological_weight
        self.lexical_weight = settings.retrieval_lexical_weight
        self.rrf_k = settings.rrf_k
        self.recursive_enabled = settings.recursive_expansion_enabled
        self.max_depth = settings.recursive_expansion_max_depth