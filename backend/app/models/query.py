"""
Query and Response Models.

Additional models for intent classification, agentic correction,
and hybrid retrieval scoring.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .document import QueryIntent, RetrievalResult, QueryResponse


class IntentClassification(BaseModel):
    """Result of intent-to-pattern translation."""

    intent: QueryIntent
    confidence: float
    keywords: List[str] = Field(default_factory=list)
    structural_hints: List[str] = Field(default_factory=list)
    suggested_expansion: bool = False


class AgenticCorrection(BaseModel):
    """Record of an agentic self-correction pass."""

    pass_number: int
    missing_dependencies: List[UUID] = Field(default_factory=list)
    added_nodes: List[UUID] = Field(default_factory=list)
    added_edges: List[UUID] = Field(default_factory=list)
    confidence_before: float
    confidence_after: float
    triggered: bool = False


class HybridSearchRequest(BaseModel):
    """Request for hybrid pattern-semantic search."""

    query: str
    intent: Optional[QueryIntent] = None
    top_k: int = 10
    semantic_weight: float = 0.4
    topological_weight: float = 0.4
    lexical_weight: float = 0.2
    rrf_k: int = 60
    enable_recursive_expansion: bool = True
    max_expansion_depth: int = 3