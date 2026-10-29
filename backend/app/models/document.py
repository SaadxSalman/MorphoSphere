"""
Document Data Models for MorphoSphere.

Defines the core data structures for ingested documents, code files,
structural motifs, and graph nodes used throughout the pipeline.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types for ingestion."""
    CODE = "code"
    DOCUMENTATION = "documentation"
    SPECIFICATION = "specification"
    LOG = "log"
    CONFIG = "config"
    UNKNOWN = "unknown"


class Language(str, Enum):
    """Programming languages supported by Tree-sitter parsers."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    CPP = "cpp"
    UNKNOWN = "unknown"


class MotifType(str, Enum):
    """Types of structural motifs that can be extracted."""
    DESIGN_PATTERN = "design_pattern"
    STATE_MACHINE = "state_machine"
    API_ENDPOINT = "api_endpoint"
    DATABASE_TRANSACTION = "database_transaction"
    CLASS_HIERARCHY = "class_hierarchy"
    FUNCTION_CALL_GRAPH = "function_call_graph"
    IMPORT_DEPENDENCY = "import_dependency"
    ERROR_HANDLING = "error_handling"
    UNKNOWN = "unknown"


class QueryIntent(str, Enum):
    """Intent categories for user queries."""
    BEHAVIORAL_FLOW = "behavioral_flow"
    STRUCTURAL_BUG = "structural_bug"
    ARCHITECTURAL_RELATIONSHIP = "architectural_relationship"
    CODE_SEARCH = "code_search"
    DOCUMENTATION_LOOKUP = "documentation_lookup"
    UNKNOWN = "unknown"


# -------------------------------------------------------------------------
# Core Document Models
# -------------------------------------------------------------------------

class DocumentNode(BaseModel):
    """A node in the Abstract Syntax Graph representing a code/document element."""

    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    node_type: str  # e.g., "function", "class", "interface", "module", "section"
    name: str
    language: Language = Language.UNKNOWN
    file_path: str
    start_line: int
    end_line: int
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    parent_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentEdge(BaseModel):
    """A directed edge in the Abstract Syntax Graph representing a relationship."""

    id: UUID = Field(default_factory=uuid4)
    source_node_id: UUID
    target_node_id: UUID
    edge_type: str  # e.g., "calls", "imports", "extends", "implements", "contains"
    weight: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class IngestedDocument(BaseModel):
    """A fully ingested document with its ASG nodes and edges."""

    id: UUID = Field(default_factory=uuid4)
    filename: str
    file_path: str
    document_type: DocumentType
    language: Language = Language.UNKNOWN
    content: str
    size_bytes: int
    node_count: int = 0
    edge_count: int = 0
    motif_count: int = 0
    ingestion_timestamp: datetime = Field(default_factory=datetime.utcnow)
    checksum: str = ""
    nodes: List[DocumentNode] = Field(default_factory=list)
    edges: List[DocumentEdge] = Field(default_factory=list)
    motifs: List["StructuralMotif"] = Field(default_factory=list)


# -------------------------------------------------------------------------
# Structural Motif Models
# -------------------------------------------------------------------------

class StructuralMotif(BaseModel):
    """A discovered structural motif (recurring pattern) in code/docs."""

    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    motif_type: MotifType
    name: str
    description: str
    node_ids: List[UUID] = Field(default_factory=list)
    frequency: int = 1
    confidence: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------------------------------------------------------
# Query & Retrieval Models
# -------------------------------------------------------------------------

class QueryRequest(BaseModel):
    """User query request for the retrieval engine."""

    query: str
    intent: Optional[QueryIntent] = None
    top_k: int = 10
    include_graph: bool = True
    enable_agentic_correction: bool = True


class RetrievalResult(BaseModel):
    """A single retrieval result with semantic and topological scores."""

    document_id: UUID
    node_id: Optional[UUID] = None
    content: str
    semantic_score: float
    topological_score: float
    lexical_score: float
    fused_score: float
    motif_matches: List[UUID] = Field(default_factory=list)
    graph_neighbors: List[DocumentNode] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    """Complete response from the retrieval and generation pipeline."""

    query: str
    intent: QueryIntent
    results: List[RetrievalResult]
    generated_answer: str
    confidence: float
    agentic_passes: int = 0
    graph_context: List[DocumentNode] = Field(default_factory=list)
    processing_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Forward reference resolution
IngestedDocument.model_rebuild()