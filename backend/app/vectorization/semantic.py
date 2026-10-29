"""
Semantic Embedding Provider.

Generates dense vector embeddings for text content using either
a local sentence-transformers model or an Ollama embedding endpoint.
Falls back to a deterministic hash-based vector when no provider is available.
"""

import logging
from typing import List

import numpy as np

logger = logging.getLogger(__name__)


class SemanticEmbedder:
    """Produces semantic (contextual) embeddings for text."""

    def __init__(self) -> None:
        self._model = None
        self._model_name = "all-MiniLM-L6-v2"
        self._available = False
        self._vector_size = 768

    def _ensure_model(self) -> None:
        """Lazy-load the sentence-transformers model if available."""
        if self._available or self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
            self._vector_size = self._model.get_sentence_embedding_dimension()
            self._available = True
            logger.info("Loaded sentence-transformers model: %s", self._model_name)
        except ImportError:
            logger.warning(
                "sentence-transformers not installed. Using hash-based fallback embeddings."
            )
            self._available = False

    def embed_text(self, text: str) -> List[float]:
        """
        Embed a text string into a dense vector.

        Returns a list of floats of length _vector_size.
        """
        if not text:
            return [0.0] * self._vector_size

        self._ensure_model()

        if self._available and self._model is not None:
            try:
                vec = self._model.encode(text, convert_to_numpy=True)
                return vec.tolist()
            except Exception as exc:  # noqa: BLE001
                logger.warning("Embedding model failed, using fallback: %s", exc)

        # Fallback: deterministic hash-based vector
        return self._hash_fallback(text)

    def _hash_fallback(self, text: str) -> List[float]:
        """Generate a deterministic pseudo-vector from text hash."""
        import hashlib

        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        vec = []
        for i in range(0, len(h), 2):
            byte_val = int(h[i:i + 2], 16)
            vec.append((byte_val - 127.5) / 127.5)
        # Pad or truncate to _vector_size
        if len(vec) < self._vector_size:
            vec.extend([0.0] * (self._vector_size - len(vec)))
        return vec[: self._vector_size]


# Singleton instance
semantic_embedder = SemanticEmbedder()