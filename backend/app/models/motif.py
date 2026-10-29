"""
Motif Data Models.

Additional models for structural motif representation and graph serialization.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .document import MotifType


class MotifNode(BaseModel):
    """A node within a structural motif subgraph."""

    id: UUID = Field(default_factory=uuid4)
    motif_id: UUID
    label: str
    node_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class MotifEdge(BaseModel):
    """An edge within a structural motif subgraph."""

    id: UUID = Field(default_factory=uuid4)
    motif_id: UUID
    source_id: UUID
    target_id: UUID
    relationship: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class MotifGraph(BaseModel):
    """A complete structural motif as a graph."""

    id: UUID = Field(default_factory=uuid4)
    motif_type: MotifType
    name: str
    description: str
    nodes: List[MotifNode] = Field(default_factory=list)
    edges: List[MotifEdge] = Field(default_factory=list)
    frequency: int = 1
    confidence: float = 0.0