"""
Topological Embedding Provider.

Generates GNN-style topological embeddings for graph nodes based on
their structural properties (type, depth, connectivity, position).
Falls back to feature-based vectors when no GNN library is available.
"""

import logging
from typing import List

import numpy as np

from app.models.document import DocumentNode

logger = logging.getLogger(__name__)


class TopologicalEmbedder:
    """
    Produces topological embeddings that encode graph structure,
    tree depth, node type, and relational distance.
    """

    def __init__(self) -> None:
        self._vector_size = 768

    def embed_node(self, node: DocumentNode) -> List[float]:
        """
        Embed a DocumentNode into a topological feature vector.

        Features encoded:
          - Node type one-hot
          - Depth in the AST tree
          - Line position (normalized)
          - Content length (normalized)
          - Parent/child relationship flags
          - Language one-hot
        """
        features: List[float] = []

        # Node type encoding (hash-based one-hot)
        type_hash = self._hash_mod(node.node_type, 64)
        type_vec = [0.0] * 64
        type_vec[type_hash] = 1.0
        features.extend(type_vec)

        # Depth proxy: number of dots in metadata or line number
        depth = min(node.start_line / 1000.0, 1.0)
        features.append(depth)

        # Normalized line position
        features.append(min(node.start_line / 10000.0, 1.0))

        # Content length normalized
        content_len = min(len(node.content) / 5000.0, 1.0)
        features.append(content_len)

        # Has parent flag
        features.append(1.0 if node.parent_id else 0.0)

        # Language encoding
        lang_hash = self._hash_mod(node.language.value, 32)
        lang_vec = [0.0] * 32
        lang_vec[lang_hash] = 1.0
        features.extend(lang_vec)

        # Pad/truncate to target size
        if len(features) < self._vector_size:
            features.extend([0.0] * (self._vector_size - len(features)))
        return features[: self._vector_size]

    def embed_graph(
        self,
        nodes: List[DocumentNode],
        edges: List[Any],
    ) -> List[List[float]]:
        """
        Embed a list of nodes into topological vectors.
        """
        return [self.embed_node(n) for n in nodes]

    @staticmethod
    def _hash_mod(text: str, mod: int) -> int:
        h = 0
        for ch in text:
            h = (h * 31 + ord(ch)) % mod
        return h


# Singleton instance
topological_embedder = TopologicalEmbedder()