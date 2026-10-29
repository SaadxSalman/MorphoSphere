# MorphoSphere — Topological & Structural Pattern Engine

> **An advanced generative artificial intelligence knowledge engine that replaces naive text splitting with multi-dimensional structural pattern recognition, Abstract Syntax Graph (ASG) parsing, and latent topological matching for complex codebases, system logs, and interconnected technical documentation.**

---

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Architecture](#architecture)
5. [Core Components](#core-components)
   - [Multi-Modal Ingestion & Topological Parsing Layer](#1-multi-modal-ingestion--topological-parsing-layer)
   - [Abstract Syntax Graph (ASG) Parsing](#abstract-syntax-graph-asg-parsing)
   - [Structural Motif Extraction](#structural-motif-extraction)
   - [Dual-Space Latent Vectorization](#2-dual-space-latent-vectorization)
   - [Hybrid Pattern-Semantic Retrieval Engine](#3-hybrid-pattern-semantic-retrieval-engine)
   - [Reciprocal Rank Fusion (RRF)](#reciprocal-rank-fusion-rrf)
   - [Agentic Self-Correction Loop](#4-agentic-self-correction-loop)
6. [Tech Stack](#tech-stack)
7. [Directory Layout](#directory-layout)
8. [Data Models](#data-models)
9. [Configuration (.env)](#configuration-env)
10. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Docker Deployment (Recommended)](#docker-deployment-recommended)
    - [Manual Deployment](#manual-deployment)
11. [Usage](#usage)
    - [Starting the Stack](#starting-the-stack)
    - [Ingesting Code](#ingesting-code)
    - [Querying the Engine](#querying-the-engine)
    - [Graph Visualization](#graph-visualization)
12. [API Reference](#api-reference)
    - [Health & Info](#health--info)
    - [Ingestion Endpoints](#ingestion-endpoints)
    - [Retrieval Endpoints](#retrieval-endpoints)
    - [Graph Endpoints](#graph-endpoints)
13. [Frontend](#frontend)
14. [Environment Variables](#environment-variables)
15. [Security](#security)
16. [Extending MorphoSphere](#extending-morphosphere)
17. [Troubleshooting](#troubleshooting)
18. [Roadmap](#roadmap)
19. [Contributing](#contributing)
20. [License](#license)
21. [Acknowledgments](#acknowledgments)

---

## Overview

**MorphoSphere** is a full-stack, production-ready generative AI knowledge engine designed for deep structural understanding of software systems. Traditional retrieval-augmented generation (RAG) systems treat documents as flat streams of text, splitting them into fixed-size chunks that sever structural boundaries, break dependency chains, and obscure macro-level design patterns.

MorphoSphere takes a fundamentally different approach: it treats codebases, system logs, and technical documentation as **topological graphs filled with recurring behavioral and structural motifs**. By combining Abstract Syntax Graph (ASG) parsing, dual-space vectorization (semantic + topological), hybrid retrieval with Reciprocal Rank Fusion (RRF), and an agentic self-correction loop, MorphoSphere retrieves context that preserves structural integrity and delivers technically accurate, architecture-aware answers.

### Key Differentiators

| Feature | Traditional RAG | MorphoSphere |
|---------|----------------|--------------|
| Chunking | Fixed-size character/token splitting | AST-aware structural parsing |
| Graph Awareness | None (flat vectors) | Neo4j-backed Abstract Syntax Graph |
| Structural Patterns | Not detected | Motif extraction (design patterns, APIs, transactions) |
| Vector Spaces | Single semantic space | Dual-space: semantic + topological |
| Retrieval | Semantic similarity only | Hybrid: lexical + semantic + topological + RRF |
| Self-Correction | None | Agentic recursive dependency expansion |
| Context Integrity | Fragmented | Structure-preserving |

## Problem Statement

Standard document retrieval architectures fail when faced with:

1. **Deeply nested architecture** — Fixed-size chunks cut across class boundaries, function definitions, and module imports, losing the structural context needed to understand how pieces fit together.

2. **Legacy codebases** — Without structural understanding, a retrieval system cannot distinguish between an interface declaration and its implementation, or between a database transaction block and a standalone query.

3. **Complex multi-file documentation** — Cross-references between specification documents, API references, and code examples are lost when documents are chunked independently.

4. **Behavioral flows** — Understanding a system's runtime behavior requires tracing call chains, state transitions, and dependency graphs — impossible with flat text embeddings alone.

5. **Structural bugs** — A bug in one file may be caused by a missing implementation in another. Naive retrieval returns the interface but not the implementation, leading to incomplete or incorrect answers.

---

## Solution

MorphoSphere solves these problems through a four-layer architecture:

### Layer 1: Multi-Modal Ingestion & Topological Parsing

Instead of fixed-size character chunking, ingestion leverages domain-specific structural parsers:

- **Tree-sitter** for multi-language AST parsing (Python, JavaScript, TypeScript, Go, Rust, Java, C++)
- **Abstract Syntax Graphs (ASGs)** — Code and specs are compiled into syntax and dependency graphs
- **Structural Motif Extraction** — Identifies recurring design patterns (factory patterns, API state-machine transitions, database transaction blocks) and tags them as discrete structural nodes

### Layer 2: Dual-Space Latent Vectorization

The indexing layer maintains **two synchronized vector spaces**:

- **Semantic Space** — Traditional dense embeddings (via sentence-transformers or Ollama) to capture contextual intent
- **Topological Motif Space** — Graph neural network (GNN)-style embeddings that encode structural topology, tree depth, and relational distance between components

### Layer 3: Hybrid Pattern-Semantic Retrieval Engine

When a user submits a complex technical query, retrieval executes a multi-stage funnel:

1. **Intent-to-Pattern Translation** — A lightweight classifier parses the query to determine if the user is looking for a behavioral flow, a structural bug, or an architectural relationship
2. **Sub-Graph Isomorphism & Vector Search** — Combines BM25 lexical matching for precise identifiers, dense vector similarity for semantics, and structural graph retrieval (via Neo4j or NetworkX) to fetch surrounding dependency trees
3. **Reciprocal Rank Fusion (RRF)** — Dynamically merges semantic scores and structural topology scores to extract the most accurate context window

### Layer 4: Agentic Self-Correction Loop

A built-in validation agent inspects retrieved structural traces before generation:

- If a structural dependency is broken or incomplete (e.g., an interface is retrieved without its corresponding implementation class), the agent triggers a **recursive expansion pass**, pulling adjacent graph nodes automatically
- Up to 3 recursive passes by default, with configurable confidence thresholds

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MORPHOSPHERE STACK                            │
├─────────────────┬─────────────────┬─────────────────┬───────────────────┤
│   FRONTEND      │     BACKEND     │   GRAPH DB      │   VECTOR DB       │
│   (React/Vite)  │  (FastAPI)      │   (Neo4j)       │   (Qdrant)        │
│                 │                 │                 │                   │
│ • Query Panel   │ • Ingestion     │ • ASG Storage   │ • Semantic Space  │
│ • Ingestion     │ • Retrieval     │ • Motif Graph   │ • Topological     │
│ • Graph View    │ • Agentic Loop  │ • Cypher Queries│   Motif Space     │
│ • Health Panel  │ • REST API      │                 │                   │
└─────────────────┴─────────────────┴─────────────────┴───────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   LLM Runtime   │
                    │  (Ollama/vLLM)  │
                    │  Qwen2.5-Coder  │
                    └─────────────────┘
```

### Data Flow

1. **Ingestion**: Source files → Tree-sitter ASG parser → Neo4j (graph) + Qdrant (vectors)
2. **Retrieval**: User query → Intent classifier → Parallel search (semantic + topological + lexical) → RRF fusion → Graph expansion → Agentic validation → LLM generation
3. **Response**: Structured answer with source citations, confidence scores, and graph context

---

## Core Components

### 1. Multi-Modal Ingestion & Topological Parsing Layer

#### Ingestion Pipeline (`backend/app/ingestion/pipeline.py`)

The ingestion pipeline orchestrates the complete end-to-end flow:

1. **File Reading** — Reads source code and documentation files from disk
2. **Checksum Computation** — SHA-256 hash for change detection and deduplication
3. **Document Classification** — Auto-detects document type (code, documentation, specification, log, config) and programming language
4. **ASG Parsing** — Tree-sitter parses source files into Abstract Syntax Graphs
5. **Motif Extraction** — Discovers structural motifs (design patterns, API endpoints, imports, error handling)
6. **Graph Storage** — Nodes and edges persisted to Neo4j
7. **Vector Indexing** — Semantic and topological embeddings stored in Qdrant

#### Directory Ingestion

Recursively ingests all supported files in a directory with configurable file extensions:

```bash
POST /api/v1/ingest/directory?directory_path=/path/to/project&extensions=py,js,ts,go
```

### Abstract Syntax Graph (ASG) Parsing

The ASG parser (`backend/app/ingestion/parser.py`) uses **Tree-sitter** to parse source code into graph structures:

- **Nodes**: Functions, classes, interfaces, methods, imports, function calls, control structures (if/for/while/try), enums, structs, traits
- **Edges**: Contains (parent-child), calls, imports, extends, implements
- **Language Support**: Python, JavaScript, TypeScript, Go, Rust, Java, C++
- **Fallback Mode**: When Tree-sitter is unavailable, treats entire files as single nodes

Example ASG structure:
```
Module (file: auth.py)
├── Class: AuthManager
│   ├── Function: authenticate()
│   │   ├── Call: validate_credentials()
│   │   └── Call: create_session()
│   └── Function: logout()
├── Import: from database import Connection
└── Import: from crypto import hash_password
```

### Structural Motif Extraction

The motif extractor (`backend/app/ingestion/motifs.py`) identifies recurring patterns:

| Motif Type | Description | Detection Heuristic |
|------------|-------------|---------------------|
| `class_hierarchy` | Class definitions and inheritance | `class_definition` / `class_declaration` nodes |
| `api_endpoint` | API route handlers | Functions with route decorators (`@app.route`, `@router.get`, etc.) |
| `import_dependency` | Import statements | `import_statement`, `import_from_statement` nodes |
| `error_handling` | Try/except blocks | `try_statement` nodes |
| `state_machine` | State transition patterns | Detects state-related method naming |
| `database_transaction` | Transaction blocks | Detects `begin`, `commit`, `rollback` patterns |
| `design_pattern` | Factory, Singleton, etc. | Pattern-specific structural signatures |



### 2. Dual-Space Latent Vectorization

#### Semantic Embeddings (`backend/app/vectorization/semantic.py`)

Dense vector representations of textual content:

- **Primary**: Sentence-Transformers (`all-MiniLM-L6-v2`) — 384-dimensional dense vectors
- **Fallback**: Deterministic SHA-256 hash-based pseudo-vectors (when no ML libraries available)
- **Usage**: Captures contextual intent, natural language meaning, documentation semantics

#### Topological Embeddings (`backend/app/vectorization/topological.py`)

Graph-structure-aware vectors encoding:

- Node type one-hot encoding (64 dimensions)
- Tree depth proxy (normalized line number)
- Content length normalization
- Parent/child relationship flags
- Language one-hot encoding (32 dimensions)
- **Total**: 768-dimensional feature vectors

#### Qdrant Collections

| Collection | Purpose | Vector Size | Distance |
|------------|---------|-------------|----------|
| `morpho_semantic` | Semantic similarity search | 768 | Cosine |
| `morpho_topological` | Topological structure search | 768 | Cosine |


### 3. Hybrid Pattern-Semantic Retrieval Engine

#### Intent Classification (`backend/app/retrieval/intent.py`)

Classifies user queries into intent categories:

| Intent | Keywords | Use Case |
|--------|----------|----------|
| `behavioral_flow` | flow, behavior, execution, runtime, pipeline | Understanding how code executes |
| `structural_bug` | bug, error, issue, broken, fix, crash | Finding structural defects |
| `architectural_relationship` | architecture, structure, dependency, interface | Understanding system design |
| `code_search` | find, search, where is, locate | Locating specific code elements |
| `documentation_lookup` | documentation, doc, readme, spec | Finding documentation |

#### Parallel Search Strategies

| Strategy | Source | Method |
|----------|--------|--------|
| Semantic | Qdrant `morpho_semantic` | Dense vector cosine similarity |
| Topological | Qdrant `morpho_topological` | GNN-style structural vector search |
| Lexical | Neo4j Cypher | BM25-style keyword matching on node content |

#### Reciprocal Rank Fusion (RRF)

Results from all three strategies are fused using RRF:

```
RRF(score) = Σ (weight_i / (k + rank_i))
```

Where:
- `k = 60` (configurable RRF constant)
- `weight_i` = strategy weight (semantic: 0.4, topological: 0.4, lexical: 0.2)
- `rank_i` = position of the result in strategy i's ranked list

This ensures that results ranking highly across multiple strategies surface to the top, even if no single strategy ranks them #1.

### 4. Agentic Self-Correction Loop

The validation agent (`backend/app/agent/validation.py`) operates after initial retrieval:

1. **Dependency Check** — Verifies that retrieved nodes have their structural dependencies (e.g., if an interface is retrieved, check for its implementation)
2. **Missing Dependency Detection** — Uses Neo4j Cypher queries to find nodes that reference others without reciprocal connections
3. **Recursive Expansion** — Pulls adjacent graph nodes (depth 1) for missing dependencies
4. **Confidence Tracking** — Computes aggregate confidence before and after each pass
5. **Termination** — Stops when confidence exceeds threshold (default 0.75) or max passes reached (default 3)

---

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Backend Framework | FastAPI | 0.115.0 | REST API, async request handling |
| ASG Parsing | Tree-sitter | 0.23.0 | Multi-language AST parsing |
| Graph Database | Neo4j | 5.15 | Topological relationship storage |
| Vector Database | Qdrant | latest | Dual-space vector storage |
| LLM Runtime | Ollama | latest | Local LLM inference (Qwen2.5-Coder) |
| Embeddings | Sentence-Transformers | 3.0.1 | Semantic embedding generation |
| Graph Algorithms | NetworkX | 3.3 | Graph analysis utilities |
| Workflow | LangGraph | 0.2.27 | Pipeline orchestration |
| Frontend | React + Vite | 18.3.1 | Web UI |
| Styling | Tailwind CSS | 3.4.15 | Utility-first CSS |
| Icons | Lucide React | 0.453.0 | Icon library |
| Container | Docker | — | Service orchestration |

---

## Directory Layout

```
MorphoSphere/
├── .env                          # All secrets and configuration (GITIGNORED)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── docker-compose.yml            # Multi-service Docker orchestration
├── requirements.txt              # Python dependencies
│
├── backend/
│   ├── Dockerfile.backend        # Backend container image
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI application entry point
│       ├── config.py             # Pydantic settings from .env
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py         # All REST API endpoints
│       │   └── dependencies.py   # Dependency injection
│       ├── models/
│       │   ├── __init__.py
│       │   ├── document.py       # DocumentNode, IngestedDocument, etc.
│       │   ├── motif.py          # StructuralMotif, MotifGraph
│       │   └── query.py          # QueryRequest, QueryResponse, IntentClassification
│       ├── database/
│       │   ├── __init__.py
│       │   ├── neo4j_client.py   # Neo4j graph database client
│       │   └── qdrant_client.py  # Qdrant vector database client
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── parser.py         # Tree-sitter ASG parser
│       │   ├── motifs.py         # Structural motif extraction
│       │   └── pipeline.py       # End-to-end ingestion pipeline
│       ├── vectorization/
│       │   ├── __init__.py
│       │   ├── semantic.py       # Semantic embedding provider
│       │   └── topological.py    # Topological embedding provider
│       ├── retrieval/
│       │   ├── __init__.py
│       │   ├── hybrid.py         # Hybrid pattern-semantic retrieval
│       │   ├── intent.py         # Intent-to-pattern classification
│       │   └── rrf.py            # Reciprocal Rank Fusion
│       ├── agent/
│       │   ├── __init__.py
│       │   └── validation.py     # Agentic self-correction loop
│       └── langgraph/
│           ├── __init__.py
│           └── workflow.py       # LangGraph workflow orchestration
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Main application with tab navigation
        └── components/
            ├── QueryPanel.jsx    # Structural query interface
            ├── IngestionPanel.jsx # File/directory ingestion
            ├── GraphView.jsx     # ASG graph visualization
            └── HealthPanel.jsx   # System health monitoring
```


---

## Data Models

### DocumentNode

Represents a single node in the Abstract Syntax Graph:

```python
class DocumentNode(BaseModel):
    id: UUID
    document_id: UUID
    node_type: str        # "function_definition", "class_definition", etc.
    name: str
    language: Language    # python, javascript, typescript, go, rust, java, cpp
    file_path: str
    start_line: int
    end_line: int
    content: str
    metadata: dict
    parent_id: Optional[UUID]
```

### DocumentEdge

Represents a directed relationship between two nodes:

```python
class DocumentEdge(BaseModel):
    id: UUID
    source_node_id: UUID
    target_node_id: UUID
    edge_type: str        # "contains", "calls", "imports", "extends", "implements"
    weight: float
    metadata: dict
```

### IngestedDocument

A complete ingested document with ASG nodes, edges, and motifs:

```python
class IngestedDocument(BaseModel):
    id: UUID
    filename: str
    file_path: str
    document_type: DocumentType
    language: Language
    content: str
    size_bytes: int
    nodes: List[DocumentNode]
    edges: List[DocumentEdge]
    motifs: List[StructuralMotif]
    checksum: str
```

### QueryResponse

The complete response from a query:

```python
class QueryResponse(BaseModel):
    query: str
    intent: QueryIntent
    results: List[RetrievalResult]
    generated_answer: str
    confidence: float
    agentic_passes: int
    graph_context: List[DocumentNode]
    processing_time_ms: float
    timestamp: datetime
```

---

## Configuration (.env)

All configuration is centralized in `.env` at the project root. **This file is gitignored and must never be committed.**

Create `.env` from the template below (already provided in the repository):

```bash
# Application
APP_NAME=MorphoSphere
APP_ENV=development
DEBUG=true
PORT=8000

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=morphosphere_neo4j_secret_2024

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_SEMANTIC=morpho_semantic
QDRANT_COLLECTION_TOPOLOGICAL=morpho_topological
QDRANT_VECTOR_SIZE=768

# LLM
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5-coder:7b

# Retrieval
RETRIEVAL_TOP_K=10
RETRIEVAL_SEMANTIC_WEIGHT=0.4
RETRIEVAL_TOPOLOGICAL_WEIGHT=0.4
RETRIEVAL_LEXICAL_WEIGHT=0.2
RRF_K=60

# Agent
AGENT_VALIDATION_ENABLED=true
AGENT_MAX_RECURSION_PASSES=3
AGENT_CONFIDENCE_THRESHOLD=0.75

# Security
SECRET_KEY=change-this-in-production
```

**Important**: Never commit `.env` to version control. It is listed in `.gitignore`.


---

## Installation

### Prerequisites

- **Docker & Docker Compose** (recommended deployment)
- **Python 3.11+** (for manual backend deployment)
- **Node.js 18+** (for manual frontend deployment)
- **8GB+ RAM** recommended (Neo4j + Qdrant + Ollama)

### Docker Deployment (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SaadxSalman/MorphoSphere.git
   cd MorphoSphere
   ```

2. **Configure environment**:
   ```bash
   # .env is already provided and gitignored
   # Edit it if you need to customize ports, passwords, or model names
   ```

3. **Pull required Ollama models**:
   ```bash
   # Start Ollama first, then pull models
   docker run -d -p 11434:11434 --name ollama ollama/ollama
   docker exec ollama ollama pull qwen2.5-coder:7b
   docker exec ollama ollama pull nomic-embed-text
   ```

4. **Start all services**:
   ```bash
   docker-compose up -d
   ```

5. **Verify deployment**:
   - Backend API: http://localhost:8000/docs
   - Frontend UI: http://localhost:3000
   - Neo4j Browser: http://localhost:7474
   - Qdrant Dashboard: http://localhost:6333


### Manual Deployment

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure .env (already provided)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev  # Starts on http://localhost:3000
```

#### Infrastructure (Neo4j + Qdrant + Ollama)

```bash
docker-compose up -d neo4j qdrant ollama
```

---

## Usage

### Starting the Stack

```bash
# Using Docker Compose (starts everything)
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Ingesting Code

#### Via Frontend UI

1. Open http://localhost:3000
2. Click the **Ingest** tab
3. Enter a file path or directory path
4. Specify file extensions (comma-separated)
5. Click **Ingest File** or **Ingest Directory**

#### Via API

```bash
# Ingest a single file
curl -X POST "http://localhost:8000/api/v1/ingest/file?file_path=/path/to/code.py"

# Ingest a directory
curl -X POST "http://localhost:8000/api/v1/ingest/directory?directory_path=/path/to/project&extensions=py,js,ts"
```

### Querying the Engine

#### Via Frontend UI

1. Open http://localhost:3000
2. Stay on the **Query** tab (default)
3. Enter your technical question
4. Optionally select an intent category
5. Toggle **Agentic Self-Correction** if needed
6. Click **Analyze Structure**

#### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does the authentication flow connect to the database layer?",
    "intent": "behavioral_flow",
    "top_k": 10,
    "enable_agentic_correction": true
  }'
```

#### Example Queries

| Query | Intent | What it finds |
|-------|--------|---------------|
| "Show me the factory pattern implementations" | `architectural_relationship` | All factory pattern classes and their relationships |
| "Why is the database connection leaking?" | `structural_bug` | Database transaction blocks without proper cleanup |
| "Trace the request flow from API to database" | `behavioral_flow` | Complete call chain from controller to repository |
| "Find the user authentication middleware" | `code_search` | Authentication-related functions and classes |
| "What does the configuration module do?" | `documentation_lookup` | Configuration documentation and code |

### Graph Visualization

1. Click the **Graph** tab in the frontend
2. Adjust the **Max Nodes** slider (default: 100)
3. Click **Refresh Graph**
4. Browse the node table and edge list

The graph visualization shows:
- **Nodes**: Code elements (functions, classes, imports, etc.)
- **Edges**: Relationships (calls, imports, extends, implements, contains)
- **Metadata**: File paths, line numbers, node types


---

## API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Health & Info

#### `GET /health`
Check the health of all services (Neo4j, Qdrant, LLM).

**Response:**
```json
{
  "neo4j": true,
  "qdrant": true,
  "llm": "ollama",
  "status": "healthy"
}
```

#### `GET /info`
Get application metadata and feature flags.

**Response:**
```json
{
  "name": "MorphoSphere",
  "version": "1.0.0",
  "environment": "development",
  "debug": true,
  "supported_languages": ["python", "javascript", "typescript", "go", "rust", "java", "cpp"],
  "features": {
    "asg_parsing": true,
    "motif_extraction": true,
    "hybrid_retrieval": true,
    "agentic_loop": true,
    "graph_visualization": true
  }
}
```

### Ingestion Endpoints

#### `POST /ingest/file`
Ingest a single file into MorphoSphere.

**Query Parameters:**
- `file_path` (string, required): Absolute path to the file
- `content` (string, optional): File content (if not provided, reads from disk)

**Response:**
```json
{
  "status": "success",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "auth.py",
  "document_type": "code",
  "language": "python",
  "node_count": 15,
  "edge_count": 8,
  "motif_count": 3,
  "size_bytes": 2048,
  "checksum": "sha256hash..."
}
```

#### `POST /ingest/directory`
Ingest all supported files in a directory recursively.

**Query Parameters:**
- `directory_path` (string, required): Absolute path to the directory
- `extensions` (string, optional): Comma-separated file extensions (e.g., `py,js,ts`)

### Retrieval Endpoints

#### `POST /query`
Submit a query to the hybrid retrieval engine.

**Request Body:**
```json
{
  "query": "string",
  "intent": "behavioral_flow|structural_bug|architectural_relationship|code_search|documentation_lookup",
  "top_k": 10,
  "enable_agentic_correction": true
}
```

**Response:**
```json
{
  "query": "string",
  "intent": "behavioral_flow",
  "results": [
    {
      "document_id": "uuid",
      "node_id": "uuid",
      "content": "...",
      "semantic_score": 0.85,
      "topological_score": 0.72,
      "lexical_score": 0.91,
      "fused_score": 0.83,
      "metadata": {}
    }
  ],
  "generated_answer": "...",
  "confidence": 0.87,
  "agentic_passes": 1,
  "graph_context": [...],
  "processing_time_ms": 245.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### `GET /query/intent-suggestions`
Get intent classification for a partial query.

**Query Parameters:**
- `q` (string, required): Partial query text

### Graph Endpoints

#### `GET /graph/node/{node_id}`
Get a single graph node by ID.

#### `GET /graph/node/{node_id}/neighbors`
Get neighboring nodes for a given node.

**Query Parameters:**
- `depth` (integer, 1-5): Traversal depth (default: 1)

#### `GET /graph/visualize`
Get a subgraph for visualization.

**Query Parameters:**
- `limit` (integer, 1-1000): Maximum nodes to return (default: 100)

**Response:**
```json
{
  "nodes": [
    {"id": "...", "label": "authenticate", "node_type": "function_definition", "file_path": "auth.py", "start_line": 42}
  ],
  "edges": [
    {"id": "...", "source": "...", "target": "...", "label": "calls", "weight": 1.0}
  ],
  "node_count": 15,
  "edge_count": 8
}
```


---

## Frontend

The React frontend provides a complete web interface:

### Tabs

| Tab | Description |
|-----|-------------|
| **Query** | Submit structural queries, view results with scores, graph context, and generated answers |
| **Ingest** | Ingest single files or entire directories with extension filtering |
| **Graph** | Visualize the Abstract Syntax Graph with nodes and edges |
| **Health** | Monitor Neo4j, Qdrant, and LLM service status |

### Features

- Real-time intent detection as you type
- Agentic self-correction toggle
- Copy-to-clipboard for generated answers
- Score badges (semantic, topological, lexical, fused)
- Graph context visualization
- Service health monitoring with status badges

---

## Environment Variables

Complete reference of all `.env` variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | MorphoSphere | Application name |
| `APP_ENV` | development | Environment (development/production) |
| `DEBUG` | true | Debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `HOST` | 0.0.0.0 | Bind host |
| `PORT` | 8000 | Backend port |
| `API_V1_STR` | /api/v1 | API version prefix |
| `FRONTEND_PORT` | 3000 | Frontend port |
| `FRONTEND_URL` | http://localhost:3000 | Frontend URL |
| `BACKEND_URL` | http://localhost:8000 | Backend URL |
| `LLM_PROVIDER` | ollama | LLM provider (ollama/vllm/openai) |
| `LLM_BASE_URL` | http://localhost:11434 | LLM API base URL |
| `LLM_MODEL` | qwen2.5-coder:7b | LLM model name |
| `LLM_API_KEY` | | LLM API key (if required) |
| `LLM_TEMPERATURE` | 0.1 | Sampling temperature |
| `LLM_MAX_TOKENS` | 4096 | Max tokens per response |
| `LLM_EMBEDDING_MODEL` | nomic-embed-text | Embedding model |
| `LLM_EMBEDDING_BASE_URL` | http://localhost:11434 | Embedding API URL |

| `NEO4J_URI` | bolt://localhost:7687 | Neo4j connection URI |
| `NEO4J_USERNAME` | neo4j | Neo4j username |
| `NEO4J_PASSWORD` | morphosphere_neo4j_secret_2024 | Neo4j password |
| `NEO4J_DATABASE` | neo4j | Neo4j database name |
| `QDRANT_HOST` | localhost | Qdrant host |
| `QDRANT_PORT` | 6333 | Qdrant HTTP port |
| `QDRANT_GRPC_PORT` | 6334 | Qdrant gRPC port |
| `QDRANT_API_KEY` | | Qdrant API key |
| `QDRANT_COLLECTION_SEMANTIC` | morpho_semantic | Semantic collection name |
| `QDRANT_COLLECTION_TOPOLOGICAL` | morpho_topological | Topological collection name |
| `QDRANT_VECTOR_SIZE` | 768 | Vector dimension |
| `QDRANT_DISTANCE` | COSINE | Distance metric |
| `TREE_SITTER_LANGUAGES` | python,javascript,typescript,go,rust,java,cpp | Supported languages |
| `TREE_SITTER_PARSE_TIMEOUT` | 30 | Parse timeout in seconds |
| `MAX_FILE_SIZE_MB` | 10 | Maximum file size for ingestion |

| `MOTIF_MIN_FREQUENCY` | 2 | Minimum motif frequency |
| `MOTIF_MAX_NODES` | 50 | Maximum nodes per motif |
| `MOTIF_SIMILARITY_THRESHOLD` | 0.85 | Motif similarity threshold |
| `MOTIF_EXTRACTION_ENABLED` | true | Enable motif extraction |
| `RETRIEVAL_TOP_K` | 10 | Default top-K results |
| `RETRIEVAL_SEMANTIC_WEIGHT` | 0.4 | Semantic weight in fusion |
| `RETRIEVAL_TOPOLOGICAL_WEIGHT` | 0.4 | Topological weight in fusion |
| `RETRIEVAL_LEXICAL_WEIGHT` | 0.2 | Lexical weight in fusion |
| `RRF_K` | 60 | RRF constant |
| `RECURSIVE_EXPANSION_MAX_DEPTH` | 3 | Max recursive expansion depth |
| `RECURSIVE_EXPANSION_ENABLED` | true | Enable recursive expansion |
| `AGENT_VALIDATION_ENABLED` | true | Enable agentic validation |
| `AGENT_MAX_RECURSION_PASSES` | 3 | Max agentic passes |
| `AGENT_DEPENDENCY_CHECK_ENABLED` | true | Enable dependency checking |
| `AGENT_CONFIDENCE_THRESHOLD` | 0.75 | Confidence threshold for stopping |

| `SECRET_KEY` | morphosphere_secret_key_change_in_production_2024 | JWT secret key |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Token expiry |
| `API_KEY_HEADER` | X-API-Key | API key header name |
| `CORS_ORIGINS` | http://localhost:3000,... | CORS allowed origins |
| `ENABLE_METRICS` | true | Enable Prometheus metrics |
| `METRICS_PORT` | 9090 | Metrics port |
| `TRACING_ENABLED` | false | Enable distributed tracing |
| `JAEGER_ENDPOINT` | | Jaeger tracing endpoint |
| `FEATURE_ASG_PARSING` | true | Enable ASG parsing |
| `FEATURE_MOTIF_EXTRACTION` | true | Enable motif extraction |
| `FEATURE_HYBRID_RETRIEVAL` | true | Enable hybrid retrieval |
| `FEATURE_AGENTIC_LOOP` | true | Enable agentic loop |
| `FEATURE_GRAPH_VISUALIZATION` | true | Enable graph visualization |

---

## Security

### Secrets Management

- All secrets are stored in `.env` (gitignored)
- `SECRET_KEY` is used for JWT token signing — **change this in production**
- `NEO4J_PASSWORD` and `QDRANT_API_KEY` should be strong, unique values
- Never commit `.env` to any version control system

### CORS

Configure `CORS_ORIGINS` to restrict which origins can access the API. By default, only localhost origins are allowed.

### API Authentication

API key authentication is supported via the `X-API-Key` header. Configure `API_KEY_HEADER` in `.env` if needed.

---

## Extending MorphoSphere

### Adding New Tree-sitter Languages

1. Add the language to `TREE_SITTER_LANGUAGES` in `.env`
2. Add the mapping in `ASGParser.SUPPORTED_LANGUAGES` (`backend/app/ingestion/parser.py`)
3. Install the tree-sitter grammar for the language

### Adding New Motif Types

1. Add a new enum value to `MotifType` in `backend/app/models/document.py`
2. Add detection logic in `MotifExtractor.extract_motifs()` (`backend/app/ingestion/motifs.py`)

### Adding New Retrieval Strategies

1. Implement the search function in `HybridRetrievalEngine` (`backend/app/retrieval/hybrid.py`)
2. Add the results list to the RRF fusion call
3. Adjust weights in `.env` or code

### Adding New Agentic Behaviors

1. Extend `ValidationAgent` in `backend/app/agent/validation.py`
2. Add new dependency check patterns or correction strategies
3. Configure via `.env` feature flags

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Neo4j connection refused | Ensure Neo4j container is running: `docker-compose logs neo4j` |
| Qdrant connection refused | Ensure Qdrant container is running: `docker-compose logs qdrant` |
| Ollama model not found | Pull the model: `docker exec ollama ollama pull qwen2.5-coder:7b` |
| Tree-sitter parse errors | The parser falls back to treating files as single nodes; check logs for details |
| No retrieval results | Ingest code first using `/ingest/file` or `/ingest/directory` |
| Frontend cannot connect to backend | Ensure `VITE_API_URL` is correct and backend is running on port 8000 |
| High memory usage | Reduce `RETRIEVAL_TOP_K` or limit ingested file count |

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Returns the status of Neo4j, Qdrant, and LLM connectivity.

---

## Roadmap

### v1.1 (Near Term)
- [ ] Full LangGraph workflow integration (currently using custom orchestration)
- [ ] Real-time graph visualization with React Flow / Cytoscape
- [ ] Incremental ingestion (file watcher with debounce)
- [ ] Multi-repository support
- [ ] Query history and saved searches

### v1.2 (Mid Term)
- [ ] GNN-based topological embeddings (PyTorch Geometric)
- [ ] Code change impact analysis
- [ ] Structural bug detection rules engine
- [ ] Performance benchmarks and optimization

### v2.0 (Long Term)
- [ ] Multi-modal support (diagrams, architecture documents, video transcripts)
- [ ] Distributed ingestion cluster
- [ ] Enterprise SSO/SAML authentication
- [ ] Self-hosted model fine-tuning pipeline
- [ ] Plugin architecture for custom parsers

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Ensure `.env` is never committed (it's gitignored)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use type hints throughout
- Add docstrings for all public classes and functions
- Write tests for new features
- Update README.md when adding user-facing features

---

## License

MIT License — see LICENSE file (to be added).

---

## Acknowledgments

- **Tree-sitter** — Incremental parsing library for AST extraction
- **Neo4j** — Graph database for topological relationship storage
- **Qdrant** — Vector database for dual-space embeddings
- **Ollama** — Local LLM runtime for quantized inference
- **FastAPI** — High-performance Python web framework
- **React + Tailwind CSS** — Modern frontend stack
- **LangGraph** — Workflow orchestration (planned integration)

---

## Support

- **Issues**: https://github.com/SaadxSalman/MorphoSphere/issues
- **Documentation**: http://localhost:8000/docs (when running)
- **Email**: opensource@morphosphere.dev

---

*MorphoSphere — Understanding code through structure, not just text.*

*Repository: https://github.com/SaadxSalman/MorphoSphere*
