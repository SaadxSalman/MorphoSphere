"""
Reciprocal Rank Fusion (RRF).

Combines ranked results from multiple retrieval sources (semantic,
topological, lexical) into a single ranked list.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def reciprocal_rank_fusion(
    ranked_lists: List[List[Dict[str, Any]]],
    k: int = 60,
    weights: Optional[List[float]] = None,
) -> List[Dict[str, Any]]:
    """
    Fuse multiple ranked result lists using Reciprocal Rank Fusion.

    Args:
        ranked_lists: List of ranked result lists, each containing dicts
                      with at least an 'id' field.
        k: RRF constant (default 60).
        weights: Optional per-list weights. If None, all lists weighted equally.

    Returns:
        Fused and re-ranked list of results with 'rrf_score' added.
    """
    if not ranked_lists:
        return []

    if weights is None:
        weights = [1.0] * len(ranked_lists)

    # Collect all unique IDs with their RRF scores
    rrf_scores: Dict[str, float] = {}
    id_to_result: Dict[str, Dict[str, Any]] = {}

    for rank_list, weight in zip(ranked_lists, weights):
        for rank, result in enumerate(rank_list, start=1):
            result_id = str(result.get("id", result.get("node_id", "")))
            if not result_id:
                continue
            rrf_scores[result_id] = rrf_scores.get(result_id, 0.0) + (
                weight / (k + rank)
            )
            if result_id not in id_to_result:
                id_to_result[result_id] = result

    # Sort by RRF score descending
    fused = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    final_results = []
    for result_id, score in fused:
        result = dict(id_to_result[result_id])
        result["rrf_score"] = score
        result["id"] = result_id
        final_results.append(result)

    return final_results


def weighted_score_fusion(
    semantic_results: List[Dict[str, Any]],
    topological_results: List[Dict[str, Any]],
    lexical_results: List[Dict[str, Any]],
    semantic_weight: float = 0.4,
    topological_weight: float = 0.4,
    lexical_weight: float = 0.2,
) -> List[Dict[str, Any]]:
    """
    Fuse results using weighted scoring instead of RRF.

    Each result's score = semantic_w * sem_score + topo_w * topo_score + lex_w * lex_score.
    """
    id_to_result: Dict[str, Dict[str, Any]] = {}
    id_to_score: Dict[str, float] = {}

    def _add(results: List[Dict[str, Any]], weight: float, score_key: str) -> None:
        for r in results:
            rid = str(r.get("id", ""))
            if not rid:
                continue
            score = r.get(score_key, r.get("score", 0.0)) * weight
            id_to_score[rid] = id_to_score.get(rid, 0.0) + score
            if rid not in id_to_result:
                id_to_result[rid] = r

    _add(semantic_results, semantic_weight, "semantic_score")
    _add(topological_results, topological_weight, "topological_score")
    _add(lexical_results, lexical_weight, "lexical_score")

    fused = sorted(id_to_score.items(), key=lambda x: x[1], reverse=True)

    final_results = []
    for rid, score in fused:
        result = dict(id_to_result[rid])
        result["fused_score"] = score
        result["id"] = rid
        final_results.append(result)

    return final_results