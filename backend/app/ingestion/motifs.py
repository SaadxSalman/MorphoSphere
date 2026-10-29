"""
Structural Motif Extraction.

Identifies recurring design patterns and structural motifs in ingested
documents, tagging them as discrete nodes for topological retrieval.
"""

import logging
from typing import Any, Dict, List
from uuid import uuid4

from app.models.document import IngestedDocument, StructuralMotif, MotifType

logger = logging.getLogger(__name__)


class MotifExtractor:
    """
    Extracts structural motifs from parsed documents.

    Motifs include design patterns, state machines, API endpoints,
    database transactions, class hierarchies, and more.
    """

    def __init__(
        self,
        min_frequency: int = 2,
        max_nodes: int = 50,
        similarity_threshold: float = 0.85,
        enabled: bool = True,
    ) -> None:
        self.min_frequency = min_frequency
        self.max_nodes = max_nodes
        self.similarity_threshold = similarity_threshold
        self.enabled = enabled

    def extract_motifs(self, document: IngestedDocument) -> List[StructuralMotif]:
        """
        Extract structural motifs from an ingested document.

        Returns a list of StructuralMotif objects.
        """
        if not self.enabled:
            return []

        motifs: List[StructuralMotif] = []
        nodes = document.nodes

        # --- Design Pattern Detection: Class Hierarchies ---
        class_nodes = [n for n in nodes if n.node_type in ("class_definition", "class_declaration")]
        for cls in class_nodes:
            motifs.append(
                StructuralMotif(
                    id=uuid4(),
                    document_id=document.id,
                    motif_type=MotifType.CLASS_HIERARCHY,
                    name=f"Class Hierarchy: {cls.name}",
                    description=f"Class definition found at {cls.file_path}:{cls.start_line}",
                    node_ids=[cls.id],
                    frequency=1,
                    confidence=0.9,
                    metadata={"file_path": cls.file_path, "start_line": cls.start_line},
                )
            )

        # --- API Endpoint Detection ---
        func_nodes = [
            n for n in nodes if n.node_type in ("function_definition", "function_declaration")
        ]
        for func in func_nodes:
            content_lower = func.content.lower()
            if any(kw in content_lower for kw in ["@app.route", "@router", "@get", "@post", "@put", "@delete", "def ", "handler"]):
                motifs.append(
                    StructuralMotif(
                        id=uuid4(),
                        document_id=document.id,
                        motif_type=MotifType.API_ENDPOINT,
                        name=f"API Endpoint: {func.name}",
                        description=f"Potential API endpoint: {func.name} at {func.file_path}:{func.start_line}",
                        node_ids=[func.id],
                        frequency=1,
                        confidence=0.8,
                        metadata={"file_path": func.file_path, "start_line": func.start_line},
                    )
                )

        # --- Import Dependency Detection ---
        import_nodes = [n for n in nodes if "import" in n.node_type.lower()]
        for imp in import_nodes:
            motifs.append(
                StructuralMotif(
                    id=uuid4(),
                    document_id=document.id,
                    motif_type=MotifType.IMPORT_DEPENDENCY,
                    name=f"Import Dependency: {imp.name}",
                    description=f"Import statement at {imp.file_path}:{imp.start_line}",
                    node_ids=[imp.id],
                    frequency=1,
                    confidence=0.85,
                    metadata={"file_path": imp.file_path, "start_line": imp.start_line},
                )
            )

        # --- Error Handling Detection ---
        error_nodes = [n for n in nodes if n.node_type in ("try_statement", "try_block")]
        for err in error_nodes:
            motifs.append(
                StructuralMotif(
                    id=uuid4(),
                    document_id=document.id,
                    motif_type=MotifType.ERROR_HANDLING,
                    name=f"Error Handling Block: {err.file_path}:{err.start_line}",
                    description=f"Try/except block at {err.file_path}:{err.start_line}",
                    node_ids=[err.id],
                    frequency=1,
                    confidence=0.9,
                    metadata={"file_path": err.file_path, "start_line": err.start_line},
                )
            )

        logger.info(
            "Extracted %d motifs from document %s", len(motifs), document.id
        )
        return motifs