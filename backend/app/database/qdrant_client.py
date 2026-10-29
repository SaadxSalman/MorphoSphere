"""
Qdrant Vector Database Client.

Manages two synchronized vector collections:
  1. Semantic space - dense embeddings for contextual intent
  2. Topological motif space - GNN embeddings for structural topology
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from qdrant_client import QdrantClient as QdrantRawClient
from qdrant_client.http import models as qmodels

from app.config import settings

logger = logging.getLogger(__name__)


class QdrantClient:
    """Wrapper around Qdrant for dual-space vector storage."""

    def __init__(self) -> None:
        self._client: Optional[QdrantRawClient] = None
        self._host = settings.qdrant_host
        self._port = settings.qdrant_port
        self._api_key = settings.qdrant_api_key
        self._vector_size = settings.qdrant_vector_size

    def connect(self) -> None:
        """Initialise the Qdrant client and ensure collections exist."""
        try:
            self._client = QdrantRawClient(
                host=self._host,
                port=self._port,
                api_key=self._api_key or None,
                prefer_grpc=False,
            )
            self._ensure_collection(self._semantic_collection)
            self._ensure_collection(self._topological_collection)
            logger.info("Connected to Qdrant at %s:%s", self._host, self._port)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Qdrant connection failed (service may not be running): %s", exc)
            self._client = None

    def close(self) -> None:
        """Close the Qdrant client."""
        if self._client:
            self._client.close()
            self._client = None

    @property
    def is_connected(self) -> bool:

    # ------------------------------------------------------------------
    # Vector Upsert / Search
    # ------------------------------------------------------------------
    def upsert_semantic(
        self,
        point_id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Upsert a point into the semantic vector collection."""
        if not self._client:
            return
        self._client.upsert(
            collection_name=self._semantic_collection,
            points=[
                qmodels.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload or {},
                )
            ],
        )

    def upsert_topological(
        self,
        point_id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Upsert a point into the topological vector collection."""
        if not self._client:
            return
        self._client.upsert(
            collection_name=self._topological_collection,
            points=[
                qmodels.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload or {},
                )
            ],
        )

    def search_semantic(
        self,
        vector: List[float],
        limit: int = 10,
        filter_payload: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search the semantic collection for similar vectors."""
        if not self._client:
            return []
        qfilter = None
        if filter_payload:
            qfilter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(key=k, match=qmodels.MatchValue(value=v))
                    for k, v in filter_payload.items()
                ]
            )
        result = self._client.search(
            collection_name=self._semantic_collection,
            query_vector=vector,
            limit=limit,
            query_filter=qfilter,
            with_payload=True,
        )
        return [
            {"id": str(r.id), "score": r.score, "payload": r.payload or {}}
            for r in result
        ]

    def search_topological(
        self,
        vector: List[float],
        limit: int = 10,
        filter_payload: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search the topological collection for similar vectors."""
        if not self._client:
            return []
        qfilter = None
        if filter_payload:
            qfilter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(key=k, match=qmodels.MatchValue(value=v))
                    for k, v in filter_payload.items()
                ]
            )
        result = self._client.search(
            collection_name=self._topological_collection,
            query_vector=vector,
            limit=limit,
            query_filter=qfilter,
            with_payload=True,
        )
        return [
            {"id": str(r.id), "score": r.score, "payload": r.payload or {}}
            for r in result
        ]


# Singleton instance
qdrant_client = QdrantClient()
        return self._client is not None

    def _ensure_collection(self, name: str) -> None:
        """Create a collection if it does not already exist."""
        if not self._client:
            return
        existing = [c.name for c in self._client.get_collections().collections]
        if name not in existing:
            self._client.create_collection(
                collection_name=name,
                vectors_config=qmodels.VectorParams(
                    size=self._vector_size,
                    distance=qmodels.Distance[self._distance],
                ),
            )
            logger.info("Created Qdrant collection: %s", name)
        self._distance = settings.qdrant_distance
        self._semantic_collection = settings.qdrant_collection_semantic
        self._topological_collection = settings.qdrant_collection_topological