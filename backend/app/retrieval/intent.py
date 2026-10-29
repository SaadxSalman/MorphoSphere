"""
Intent-to-Pattern Translation.

Analyzes user queries to classify intent (behavioral flow, structural bug,
architectural relationship, etc.) and determine retrieval strategy.
"""

import logging
import re
from typing import Any, Dict, List

from app.models.query import IntentClassification, QueryIntent

logger = logging.getLogger(__name__)


class IntentClassifier:
    """
    Lightweight intent classifier using keyword matching and heuristics.

    In production, this would be replaced by a small fine-tuned LLM.
    """

    INTENT_KEYWORDS = {
        QueryIntent.BEHAVIORAL_FLOW: [
            "flow", "behavior", "execution", "runtime", "step", "sequence",
            "process", "pipeline", "workflow", "trace", "call chain",
        ],
        QueryIntent.STRUCTURAL_BUG: [
            "bug", "error", "issue", "broken", "fix", "crash", "exception",
            "failure", "leak", "race condition", "deadlock",
        ],
        QueryIntent.ARCHITECTURAL_RELATIONSHIP: [
            "architecture", "structure", "relationship", "dependency",
            "interface", "implementation", "class hierarchy", "module",
            "component", "design pattern", "coupling",
        ],
        QueryIntent.CODE_SEARCH: [
            "find", "search", "where is", "locate", "show me", "code",
            "function", "method", "variable",
        ],
        QueryIntent.DOCUMENTATION_LOOKUP: [
            "documentation", "doc", "readme", "spec", "specification",
            "manual", "guide", "tutorial",
        ],
    }

    def classify(self, query: str) -> IntentClassification:
        """
        Classify the intent of a user query.

        Returns an IntentClassification with the detected intent,
        confidence, and suggested structural hints.
        """
        query_lower = query.lower()
        scores: Dict[QueryIntent, float] = {}
        matched_keywords: List[str] = []

        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = 0.0
            for kw in keywords:
                if kw in query_lower:
                    score += 1.0
                    matched_keywords.append(kw)
            scores[intent] = score

        if not scores or max(scores.values()) == 0:
            return IntentClassification(
                intent=QueryIntent.UNKNOWN,
                confidence=0.0,
                keywords=[],
                structural_hints=[],
                suggested_expansion=False,
            )

        best_intent = max(scores, key=scores.get)
        total_matches = sum(scores.values())
        confidence = min(scores[best_intent] / max(total_matches, 1), 1.0)

        structural_hints = self._extract_structural_hints(query)
        suggested_expansion = best_intent in (
            QueryIntent.ARCHITECTURAL_RELATIONSHIP,
            QueryIntent.BEHAVIORAL_FLOW,
            QueryIntent.STRUCTURAL_BUG,
        )

        return IntentClassification(
            intent=best_intent,
            confidence=confidence,
            keywords=matched_keywords,
            structural_hints=structural_hints,
            suggested_expansion=suggested_expansion,
        )

    def _extract_structural_hints(self, query: str) -> List[str]:
        """Extract potential structural identifiers from the query."""
        hints: List[str] = []
        # Look for camelCase, snake_case, ClassName patterns
        patterns = re.findall(
            r"\b[A-Z][a-zA-Z0-9]*\b|\b[a-z]+(?:_[a-z0-9]+)+\b|\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+\b",
            query,
        )
        hints.extend(patterns[:10])
        return hints


# Singleton instance
intent_classifier = IntentClassifier()