"""
Neo4j Graph Database Client.

Handles topological relationship tracking, Abstract Syntax Graph storage,
and structural motif graph operations using Neo4j.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, AuthError

from app.config import settings
from app.models.document import DocumentEdge, DocumentNode

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Async-friendly wrapper around the Neo4j Python driver."""

    def __init__(self) -> None:
        self._driver: Optional[Driver] = None
        self._uri = settings.neo4j_uri
        self._user = settings.neo4j_username
        self._password = settings.neo4j_password
        self._database = settings.neo4j_database

    def connect(self) -> None:
        """Establish the Neo4j driver connection."""
        try:
            self._driver = GraphDatabase.driver(
                self._uri, auth=(self._user, self._password)
            )
            self._driver.verify_connectivity()
            logger.info("Connected to Neo4j at %s", self._uri)
        except (ServiceUnavailable, AuthError) as exc:
            logger.warning("Neo4j connection failed (service may not be running): %s", exc)
            self._driver = None

    def close(self) -> None:
        """Close the driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None

    @property
    def is_connected(self) -> bool:
        return self._driver is not None

    def session(self) -> Optional[Session]:
        """Return a Neo4j session, or None if not connected."""
        if not self._driver:
            return None
        return self._driver.session(database=self._database)

    # ------------------------------------------------------------------
    # Node Operations
    # ------------------------------------------------------------------
    def create_node(self, node: DocumentNode) -> Optional[str]:
        """Create or merge a DocumentNode in the graph."""
        if not self._driver:
            return None
        with self._driver.session(database=self._database) as sess:
            result = sess.run(
                """
                MERGE (n:Node {id: $id})
                SET n.node_type = $node_type,
                    n.name = $name,
                    n.language = $language,
                    n.file_path = $file_path,
                    n.start_line = $start_line,
                    n.end_line = $end_line,
                    n.content = $content,
                    n.metadata = $metadata,
                    n.created_at = datetime($created_at)
                RETURN n.id AS id
                """,
                id=str(node.id),
                node_type=node.node_type,
                name=node.name,
                language=node.language.value,
                file_path=node.file_path,
                start_line=node.start_line,
                end_line=node.end_line,
                content=node.content,
                metadata=str(node.metadata),
                created_at=node.created_at.isoformat(),
            )
            record = result.single()
            return record["id"] if record else None

    def create_edge(self, edge: DocumentEdge) -> Optional[str]:
        """Create a relationship edge between two nodes."""
        if not self._driver:
            return None
        with self._driver.session(database=self._database) as sess:
            result = sess.run(
                """
                MATCH (a:Node {id: $source_id})
                MATCH (b:Node {id: $target_id})
                MERGE (a)-[r:RELATES_TO {edge_type: $edge_type}]->(b)
                SET r.weight = $weight,
                    r.metadata = $metadata,
                    r.created_at = datetime($created_at)
                RETURN r.id AS id
                """,
                source_id=str(edge.source_node_id),
                target_id=str(edge.target_node_id),
                edge_type=edge.edge_type,
                weight=edge.weight,
                metadata=str(edge.metadata),
                created_at=edge.created_at.isoformat(),
            )
            record = result.single()
            return record["id"] if record else None

    def get_node_neighbors(self, node_id: UUID, depth: int = 1) -> List[Dict[str, Any]]:
        """Fetch neighboring nodes up to a given depth."""
        if not self._driver:
            return []
        with self._driver.session(database=self._database) as sess:
            result = sess.run(
                f"""
                MATCH (start:Node {{id: $node_id}})
                MATCH path = (start)-[*1..{depth}]-(neighbor:Node)
                RETURN DISTINCT neighbor
                LIMIT 100
                """,
                node_id=str(node_id),
            )
            return [dict(record["neighbor"]) for record in result]

    def run_cypher(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a raw Cypher query and return records as dicts."""
        if not self._driver:
            return []
        with self._driver.session(database=self._database) as sess:
            result = sess.run(query, params or {})
            return [dict(record) for record in result]


# Singleton instance
neo4j_client = Neo4jClient()