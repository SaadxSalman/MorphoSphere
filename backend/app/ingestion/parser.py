"""
Tree-sitter Based AST Parser.

Parses source code files into Abstract Syntax Graphs (ASGs) using
domain-specific Tree-sitter grammars. Falls back gracefully when
tree-sitter is not installed or a language parser is unavailable.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.models.document import DocumentEdge, DocumentNode, Language

logger = logging.getLogger(__name__)

# Lazy import of tree-sitter
try:
    from tree_sitter_languages import get_language, get_parser

    _TREE_SITTER_AVAILABLE = True
except ImportError:  # pragma: no cover
    _TREE_SITTER_AVAILABLE = False
    logger.warning(
        "tree-sitter-languages not installed. ASG parsing will be limited."
    )


class ASGParser:
    """
    Abstract Syntax Graph Parser using Tree-sitter.

    Supports multiple programming languages and extracts nodes
    (functions, classes, interfaces, etc.) and edges
    (calls, imports, extends, implements, contains).
    """

    SUPPORTED_LANGUAGES = {
        "python": Language.PYTHON,
        "javascript": Language.JAVASCRIPT,
        "typescript": Language.TYPESCRIPT,
        "go": Language.GO,
        "rust": Language.RUST,

    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Parse a source file into nodes and edges.

        Returns a dict with keys 'nodes' and 'edges'.
        """
        path = Path(file_path)
        ext = path.suffix.lower().lstrip(".")
        language_key = self._detect_language(ext, content)

        if not language_key or not self._available:
            return self._fallback_parse(file_path, content)

        parser = self._get_parser(language_key)
        if parser is None:
            return self._fallback_parse(file_path, content)

        try:
            tree = parser.parse(bytes(content, "utf8"))
            root = tree.root_node
            nodes: List[DocumentNode] = []
            edges: List[DocumentEdge] = []
            self._traverse_tree(
                root, content, file_path, language_key, nodes, edges, parent_id=None
            )
            return {"nodes": nodes, "edges": edges, "language": language_key}
        except Exception as exc:  # noqa: BLE001
            logger.error("Tree-sitter parse error for %s: %s", file_path, exc)
            return self._fallback_parse(file_path, content)

    def _detect_language(self, ext: str, content: str) -> Optional[str]:
        """Detect the programming language from file extension and content."""
        ext_map = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "jsx": "javascript",
            "tsx": "typescript",
            "go": "go",

    def _traverse_tree(
        self,
        node: Any,
        content: str,
        file_path: str,
        language_key: str,
        nodes: List[DocumentNode],
        edges: List[DocumentEdge],
        parent_id: Optional[UUID],
        depth: int = 0,
    ) -> None:
        """Recursively traverse the Tree-sitter tree to extract nodes/edges."""
        from uuid import uuid4

        node_type = node.type
        node_text = content[node.start_byte:node.end_byte]
        node_lines = content[: node.start_byte].count("\n") + 1
        end_lines = content[: node.end_byte].count("\n") + 1

        meaningful_types = {
            "function_definition",
            "function_declaration",
            "class_definition",
            "class_declaration",
            "interface_declaration",
            "method_definition",
            "method_declaration",
            "import_statement",
            "import_from_statement",
            "include_directive",
            "function_call",
            "if_statement",
            "for_statement",
            "while_statement",
            "try_statement",
            "enum_declaration",
            "struct_declaration",
            "trait_declaration",
            "impl_block",
        }

        current_id: Optional[UUID] = None
        if node_type in meaningful_types and len(node_text.strip()) > 0:
            current_id = uuid4()
            doc_node = DocumentNode(
                id=current_id,
                document_id=uuid4(),
                node_type=node_type,
                name=node_text.strip().split("\n")[0][:100],
                language=self.SUPPORTED_LANGUAGES.get(language_key, Language.UNKNOWN),
                file_path=file_path,
                start_line=node_lines,
                end_line=end_lines,
                content=node_text[:2000],
                metadata={"byte_start": node.start_byte, "byte_end": node.end_byte},
                parent_id=parent_id,
            )
            nodes.append(doc_node)

            if parent_id:
                edges.append(
                    DocumentEdge(
                        source_node_id=parent_id,
                        target_node_id=current_id,
                        edge_type="contains",
                        weight=1.0,
                    )
                )

        for child in node.children:
            self._traverse_tree(
                child,
                content,
                file_path,
                language_key,
                nodes,
                edges,
                current_id if current_id else parent_id,
                depth + 1,
            )

    def _fallback_parse(self, file_path: str, content: str) -> Dict[str, Any]:
        """Fallback when tree-sitter is unavailable - treat file as single node."""
        from uuid import uuid4

        node = DocumentNode(
            id=uuid4(),
            document_id=uuid4(),
            node_type="file",
            name=Path(file_path).name,
            language=Language.UNKNOWN,
            file_path=file_path,
            start_line=1,
            end_line=content.count("\n") + 1,
            content=content[:2000],
            metadata={"fallback": True},
        )
        return {"nodes": [node], "edges": [], "language": "unknown"}

    def get_supported_languages(self) -> List[str]:
        """Return list of supported language identifiers."""
        return list(self.SUPPORTED_LANGUAGES.keys())
            "rs": "rust",
            "java": "java",
            "cpp": "cpp",
            "cc": "cpp",
            "cxx": "cpp",
            "h": "cpp",
            "hpp": "cpp",
        }
        return ext_map.get(ext)
        "java": Language.JAVA,
        "cpp": Language.CPP,
    }

    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self._parsers: Dict[str, Any] = {}
        self._available = _TREE_SITTER_AVAILABLE

    def _get_parser(self, language: str) -> Optional[Any]:
        """Get or create a Tree-sitter parser for the given language."""
        if not self._available:
            return None
        if language not in self._parsers:
            try:
                self._parsers[language] = get_parser(language)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to load parser for %s: %s", language, exc)
                return None
        return self._parsers[language]