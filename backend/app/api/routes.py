"""
MorphoSphere API Routes.

Defines all REST endpoints for:
  - Document ingestion
  - Hybrid pattern-semantic retrieval
  - Graph visualization
  - Health checks
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from app.api.dependencies import morpho_workflow
from app.config import settings
from app.database.neo4j_client import neo4j_client
from app.database.qdrant_client import qdrant_client
from app.models.document import DocumentType, IngestedDocument, Language
from app.models.query import (
    QueryRequest,
    QueryResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# -------------------------------------------------------------------------
# Health & System
# -------------------------------------------------------------------------

@router.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """Check the health of all MorphoSphere services."""
    return morpho_workflow.health_check()


@router.get("/info", tags=["System"])
async def app_info() -> Dict[str, Any]:

# -------------------------------------------------------------------------
# Ingestion
# -------------------------------------------------------------------------

@router.post("/ingest/file", tags=["Ingestion"])
async def ingest_file(
    file_path: str,
    content: Optional[str] = None,
    background: BackgroundTasks = None,
) -> Dict[str, Any]:
    """
    Ingest a single file into MorphoSphere.

    Parses the file into an Abstract Syntax Graph, extracts structural
    motifs, and indexes everything in Neo4j and Qdrant.
    """
    try:
        doc = morpho_workflow.ingest_and_index(file_path, content)
        return {
            "status": "success",
            "document_id": str(doc.id),
            "filename": doc.filename,
            "document_type": doc.document_type.value,
            "language": doc.language.value,
            "node_count": doc.node_count,
            "edge_count": doc.edge_count,
            "motif_count": doc.motif_count,
            "size_bytes": doc.size_bytes,
            "checksum": doc.checksum,
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("Ingestion failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/ingest/directory", tags=["Ingestion"])
async def ingest_directory(
    directory_path: str,
    extensions: Optional[str] = Query(
        None,
        description="Comma-separated list of file extensions (e.g. py,js,ts)",
    ),
) -> Dict[str, Any]:
    """
    Ingest all supported files in a directory recursively.

# -------------------------------------------------------------------------
# Retrieval
# -------------------------------------------------------------------------

@router.post("/query", response_model=QueryResponse, tags=["Retrieval"])
async def query(request: QueryRequest) -> QueryResponse:
    """
    Submit a query to the MorphoSphere retrieval engine.

    Performs hybrid pattern-semantic retrieval with optional
    agentic self-correction and returns a generated answer.
    """
    try:
        response = morpho_workflow.query(
            query_text=request.query,
            intent=request.intent,
            top_k=request.top_k,
            enable_agentic=request.enable_agentic_correction,
        )
        return response
    except Exception as exc:  # noqa: BLE001
        logger.error("Query failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/query/intent-suggestions", tags=["Retrieval"])
async def intent_suggestions(
    q: str = Query(..., description="Partial query to get intent suggestions")
) -> Dict[str, Any]:
    """
    Get intent classification suggestions for a partial query.
    """
    from app.retrieval.intent import intent_classifier

    classification = intent_classifier.classify(q)
    return {

# -------------------------------------------------------------------------
# Graph
# -------------------------------------------------------------------------

@router.get("/graph/node/{node_id}", tags=["Graph"])
async def get_node(node_id: UUID) -> Dict[str, Any]:
    """Retrieve a single graph node by ID."""
    if not neo4j_client.is_connected:
        raise HTTPException(status_code=503, detail="Neo4j not available")

    records = neo4j_client.run_cypher(
        "MATCH (n:Node {id: $id}) RETURN n LIMIT 1",
        {"id": str(node_id)},
    )
    if not records:
        raise HTTPException(status_code=404, detail="Node not found")

    rec = records[0].get("n", {})
    return dict(rec)


@router.get("/graph/node/{node_id}/neighbors", tags=["Graph"])
async def get_node_neighbors(
    node_id: UUID,
    depth: int = Query(1, ge=1, le=5, description="Traversal depth"),
) -> Dict[str, Any]:
    """Get neighboring nodes for a given node."""
    if not neo4j_client.is_connected:
        raise HTTPException(status_code=503, detail="Neo4j not available")

    neighbors = neo4j_client.get_node_neighbors(node_id, depth=depth)
    return {
        "node_id": str(node_id),
        "depth": depth,
        "neighbors": neighbors,
        "count": len(neighbors),
    }


@router.get("/graph/visualize", tags=["Graph"])
async def get_graph_visualization(
    limit: int = Query(100, ge=1, le=1000, description="Maximum nodes to return"),
) -> Dict[str, Any]:
    """
    Get a subgraph suitable for visualization.

    Returns nodes and edges in a format consumable by graph
    visualization libraries (e.g., Cytoscape, D3, React Flow).
    """
    if not neo4j_client.is_connected:
        raise HTTPException(status_code=503, detail="Neo4j not available")

    records = neo4j_client.run_cypher(
        """
        MATCH (n:Node)
        WITH n LIMIT $limit
        OPTIONAL MATCH (n)-[r:RELATES_TO]->(m:Node)
        RETURN n, r, m
        """,
        {"limit": limit},
    )

    viz_nodes: List[Dict[str, Any]] = []
    viz_edges: List[Dict[str, Any]] = []
    seen_ids = set()

    for rec in records:
        n = rec.get("n", {})
        n_id = str(n.get("id", ""))
        if n_id and n_id not in seen_ids:
            seen_ids.add(n_id)
            viz_nodes.append({
                "id": n_id,
                "label": n.get("name", n_id),
                "node_type": n.get("node_type", "unknown"),
                "file_path": n.get("file_path", ""),
                "start_line": n.get("start_line", 0),
            })

        r = rec.get("r")
        m = rec.get("m")
        if r and m:
            m_id = str(m.get("id", ""))
            viz_edges.append({
                "id": str(r.get("id", "")),
                "source": n_id,
                "target": m_id,
                "label": r.get("edge_type", "relates_to"),
                "weight": r.get("weight", 1.0),
            })

    return {
        "nodes": viz_nodes,
        "edges": viz_edges,
        "node_count": len(viz_nodes),
        "edge_count": len(viz_edges),
    }
        "query": q,
        "intent": classification.intent.value,
        "confidence": classification.confidence,
        "keywords": classification.keywords,
        "structural_hints": classification.structural_hints,
        "suggested_expansion": classification.suggested_expansion,
    }
    """
    ext_list = None
    if extensions:
        ext_list = [e.strip() for e in extensions.split(",") if e.strip()]

    try:
        docs = morpho_workflow.ingestion.ingest_directory(directory_path, ext_list)
        return {
            "status": "success",
            "documents_ingested": len(docs),
            "documents": [
                {
                    "document_id": str(d.id),
                    "filename": d.filename,
                    "document_type": d.document_type.value,
                    "language": d.language.value,
                    "node_count": d.node_count,
                    "edge_count": d.edge_count,
                    "motif_count": d.motif_count,
                }
                for d in docs
            ],
        }
    except NotADirectoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("Directory ingestion failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    """Return application metadata."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "debug": settings.debug,
        "supported_languages": settings.tree_sitter_language_list,
        "features": {
            "asg_parsing": settings.feature_asg_parsing,
            "motif_extraction": settings.feature_motif_extraction,
            "hybrid_retrieval": settings.feature_hybrid_retrieval,
            "agentic_loop": settings.feature_agentic_loop,
            "graph_visualization": settings.feature_graph_visualization,
        },
    }