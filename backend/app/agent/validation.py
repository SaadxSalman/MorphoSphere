"""
Agentic Self-Correction Loop.

Validates retrieved structural traces before generation. If a structural
dependency is broken or incomplete (e.g., an interface without its
implementation), the agent triggers a recursive expansion pass to pull
adjacent graph nodes automatically.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.config import settings
from app.database.neo4j_client import neo4j_client
from app.models.document import DocumentNode
from app.models.query import AgenticCorrection, QueryResponse

logger = logging.getLogger(__name__)


class ValidationAgent:
    """
    Agent that validates retrieved graph traces and triggers recursive
    expansion when dependencies are missing or incomplete.
    """


    def validate_and_correct(
        self,
        query: str,
        results: List[Any],
        graph_context: List[DocumentNode],
    ) -> Dict[str, Any]:
        """
        Validate retrieval results and perform recursive correction if needed.

        Returns a dict with:
          - corrected_results: list of results after correction
          - graph_context: expanded graph context
          - passes: number of correction passes performed
          - corrections: list of AgenticCorrection records
        """
        if not self.enabled:
            return {
                "corrected_results": results,
                "graph_context": graph_context,
                "passes": 0,
                "corrections": [],
            }

        corrections: List[AgenticCorrection] = []
        current_results = list(results)
        current_context = list(graph_context)
        passes = 0

        for pass_num in range(1, self.max_passes + 1):
            passes = pass_num
            missing_deps: List[UUID] = []
            added_nodes: List[UUID] = []
            added_edges: List[UUID] = []

            confidence_before = self._compute_confidence(current_results)

            if self.dependency_check and neo4j_client.is_connected:
                for result in current_results:
                    if hasattr(result, "node_id") and result.node_id:
                        deps = self._check_dependencies(result.node_id)
                        if deps:
                            missing_deps.extend(deps)

            if missing_deps:
                logger.info(
                    "Pass %d: Found %d missing dependencies, expanding graph",
                    pass_num,
                    len(missing_deps),
                )
                for dep_id in missing_deps:
                    neighbors = neo4j_client.get_node_neighbors(dep_id, depth=1)
                    for nb in neighbors:
                        nb_id = UUID(nb.get("id", str(uuid4())))
                        added_nodes.append(nb_id)
                        current_context.append(
                            DocumentNode(

    def _check_dependencies(self, node_id: UUID) -> List[UUID]:
        """
        Check if a node has missing dependencies (e.g., interface without impl).

        Returns a list of node IDs that should be expanded.
        """
        missing: List[UUID] = []
        if not neo4j_client.is_connected:
            return missing

        records = neo4j_client.run_cypher(
            """
            MATCH (n:Node {id: $id})
            MATCH (n)-[:RELATES_TO]->(dep:Node)
            WHERE NOT (dep)-[:RELATES_TO]->(n)
            RETURN dep.id AS id
            LIMIT 10
            """,
            {"id": str(node_id)},
        )
        for rec in records:
            dep_id = rec.get("id")
            if dep_id:
                missing.append(UUID(dep_id))
        return missing

    def _compute_confidence(self, results: List[Any]) -> float:
        """Compute aggregate confidence for a set of results."""
        if not results:
            return 0.0
        scores = []
        for r in results:
            if hasattr(r, "fused_score"):
                scores.append(r.fused_score)
            elif hasattr(r, "score"):
                scores.append(r.score)
            elif isinstance(r, dict):
                scores.append(r.get("rrf_score", r.get("score", 0.0)))
        return sum(scores) / len(scores) if scores else 0.0


# Singleton instance
validation_agent = ValidationAgent()
                                id=nb_id,
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

                confidence_after = self._compute_confidence(current_results)
                corrections.append(
                    AgenticCorrection(
                        pass_number=pass_num,
                        missing_dependencies=missing_deps,
                        added_nodes=added_nodes,
                        added_edges=added_edges,
                        confidence_before=confidence_before,
                        confidence_after=confidence_after,
                        triggered=True,
                    )
                )

                if confidence_after >= self.confidence_threshold:
                    break
            else:
                logger.info("Pass %d: No missing dependencies. Validation passed.", pass_num)
                break

        return {
            "corrected_results": current_results,
            "graph_context": current_context,
            "passes": passes,
            "corrections": corrections,
        }
    def __init__(self) -> None:
        self.enabled = settings.agent_validation_enabled
        self.max_passes = settings.agent_max_recursion_passes
        self.dependency_check = settings.agent_dependency_check_enabled
        self.confidence_threshold = settings.agent_confidence_threshold