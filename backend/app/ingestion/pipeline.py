"""
Ingestion Pipeline.

Orchestrates the end-to-end ingestion flow:
  1. Read file content
  2. Parse into ASG (Abstract Syntax Graph) nodes/edges
  3. Extract structural motifs
  4. Store in Neo4j and Qdrant
"""

import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.config import settings
from app.database.neo4j_client import neo4j_client
from app.database.qdrant_client import qdrant_client
from app.ingestion.motifs import MotifExtractor
from app.ingestion.parser import ASGParser
from app.models.document import (
    DocumentEdge,
    DocumentNode,
    DocumentType,
    IngestedDocument,
    Language,
    StructuralMotif,
)
from app.vectorization.semantic import semantic_embedder
from app.vectorization.topological import topological_embedder

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Full ingestion pipeline for code and documentation files.
    """

    def __init__(self) -> None:
        self.parser = ASGParser(timeout=settings.tree_sitter_parse_timeout)
        self.motif_extractor = MotifExtractor(
            min_frequency=settings.motif_min_frequency,
            max_nodes=settings.motif_max_nodes,
            similarity_threshold=settings.motif_similarity_threshold,
            enabled=settings.motif_extraction_enabled,
        )

    def ingest_file(self, file_path: str, content: Optional[str] = None) -> IngestedDocument:
        """
        Ingest a single file end-to-end.
        """
        path = Path(file_path)
        if not content:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            content = path.read_text(encoding="utf-8", errors="replace")

        doc_type = self._detect_document_type(path)
        language = self._detect_language(path.suffix.lower().lstrip("."))
        checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

        document = IngestedDocument(

    def ingest_directory(self, directory_path: str, extensions: Optional[List[str]] = None) -> List[IngestedDocument]:
        """
        Ingest all supported files in a directory recursively.
        """
        if extensions is None:
            extensions = [
                "py", "js", "ts", "jsx", "tsx", "go", "rs", "java",
                "cpp", "cc", "cxx", "h", "hpp", "md", "rst", "txt",
            ]

        path = Path(directory_path)
        if not path.exists() or not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        documents: List[IngestedDocument] = []
        for ext in extensions:
            for file_path in path.rglob(f"*.{ext}"):
                try:
                    doc = self.ingest_file(str(file_path))
                    documents.append(doc)
                except Exception as exc:  # noqa: BLE001
                    logger.error("Failed to ingest %s: %s", file_path, exc)

        logger.info("Ingested %d documents from %s", len(documents), directory_path)
        return documents

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------
    def _detect_document_type(self, path: Path) -> DocumentType:
        ext = path.suffix.lower()
        code_exts = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".cpp", ".cc", ".cxx", ".h", ".hpp"}
        doc_exts = {".md", ".rst", ".txt", ".pdf", ".docx"}
        spec_exts = {".yaml", ".yml", ".json", ".xml", ".toml", ".ini", ".cfg", ".conf"}

        if ext in code_exts:
            return DocumentType.CODE
        if ext in doc_exts:
            return DocumentType.DOCUMENTATION
        if ext in spec_exts:
            return DocumentType.SPECIFICATION
        return DocumentType.UNKNOWN

    def _detect_language(self, ext: str) -> Language:
        lang_map = {
            "py": Language.PYTHON,
            "js": Language.JAVASCRIPT,
            "ts": Language.TYPESCRIPT,
            "jsx": Language.JAVASCRIPT,
            "tsx": Language.TYPESCRIPT,
            "go": Language.GO,
            "rs": Language.RUST,
            "java": Language.JAVA,
            "cpp": Language.CPP,
            "cc": Language.CPP,
            "cxx": Language.CPP,
            "h": Language.CPP,
            "hpp": Language.CPP,
        }
        return lang_map.get(ext, Language.UNKNOWN)

    def _map_language(self, lang_str: str) -> Language:
        try:
            return Language(lang_str.lower())
        except ValueError:
            return Language.UNKNOWN

    def _store_embeddings(self, document: IngestedDocument) -> None:
        """Generate semantic and topological embeddings and store in Qdrant."""
        if not qdrant_client.is_connected:
            logger.warning("Qdrant not connected, skipping embedding storage")
            return

        semantic_vector = semantic_embedder.embed_text(document.content[:4000])
        qdrant_client.upsert_semantic(
            point_id=str(document.id),
            vector=semantic_vector,
            payload={
                "document_id": str(document.id),
                "filename": document.filename,
                "file_path": document.file_path,
                "document_type": document.document_type.value,
                "language": document.language.value,
                "checksum": document.checksum,
            },
        )

        for node in document.nodes:
            node_semantic = semantic_embedder.embed_text(node.content[:1000])
            qdrant_client.upsert_semantic(
                point_id=str(node.id),
                vector=node_semantic,
                payload={
                    "node_id": str(node.id),
                    "document_id": str(document.id),
                    "node_type": node.node_type,
                    "name": node.name,
                    "file_path": node.file_path,
                    "start_line": node.start_line,
                    "end_line": node.end_line,
                },
            )

            topo_vector = topological_embedder.embed_node(node)
            qdrant_client.upsert_topological(
                point_id=str(node.id),
                vector=topo_vector,
                payload={
                    "node_id": str(node.id),
                    "document_id": str(document.id),
                    "node_type": node.node_type,
                    "name": node.name,
                    "file_path": node.file_path,
                },
            )
            id=uuid4(),
            filename=path.name,
            file_path=str(path.resolve()),
            document_type=doc_type,
            language=language,
            content=content,
            size_bytes=len(content.encode("utf-8")),
            checksum=checksum,
        )

        parse_result = self.parser.parse_file(file_path, content)
        document.nodes = parse_result.get("nodes", [])
        document.edges = parse_result.get("edges", [])
        document.language = self._map_language(parse_result.get("language", "unknown"))

        for node in document.nodes:
            node.document_id = document.id

        document.node_count = len(document.nodes)
        document.edge_count = len(document.edges)

        document.motifs = self.motif_extractor.extract_motifs(document)
        document.motif_count = len(document.motifs)

        if neo4j_client.is_connected:
            for node in document.nodes:
                neo4j_client.create_node(node)
            for edge in document.edges:
                neo4j_client.create_edge(edge)
            logger.info(
                "Stored %d nodes and %d edges in Neo4j for %s",
                document.node_count,
                document.edge_count,
                file_path,
            )

        self._store_embeddings(document)

        logger.info(
            "Ingestion complete: %s (%d nodes, %d edges, %d motifs)",
            file_path,
            document.node_count,
            document.edge_count,
            document.motif_count,
        )
        return document