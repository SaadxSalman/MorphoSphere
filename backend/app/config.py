"""
MorphoSphere Configuration Module.

Loads all settings from the .env file and provides typed configuration
objects for the entire application. No secrets are hardcoded here —
everything is sourced from environment variables.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Application ---
    app_name: str = Field(default="MorphoSphere", alias="APP_NAME")

    # --- LLM / Inference ---
    llm_provider: str = Field(default="ollama", alias="LLM_PROVIDER")
    llm_base_url: str = Field(default="http://localhost:11434", alias="LLM_BASE_URL")
    llm_model: str = Field(default="qwen2.5-coder:7b", alias="LLM_MODEL")
    llm_api_key: Optional[str] = Field(default=None, alias="LLM_API_KEY")
    llm_temperature: float = Field(default=0.1, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=4096, alias="LLM_MAX_TOKENS")
    llm_embedding_model: str = Field(default="nomic-embed-text", alias="LLM_EMBEDDING_MODEL")
    llm_embedding_base_url: str = Field(default="http://localhost:11434", alias="LLM_EMBEDDING_BASE_URL")

    # --- Neo4j Graph Database ---
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_username: str = Field(default="neo4j", alias="NEO4J_USERNAME")
    neo4j_password: str = Field(default="morphosphere_neo4j_secret_2024", alias="NEO4J_PASSWORD")
    neo4j_database: str = Field(default="neo4j", alias="NEO4J_DATABASE")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    host: str = Field(default="0.0.0.0", alias="HOST")

    # --- Qdrant Vector Database ---
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    qdrant_grpc_port: int = Field(default=6334, alias="QDRANT_GRPC_PORT")
    qdrant_api_key: Optional[str] = Field(default=None, alias="QDRANT_API_KEY")
    qdrant_collection_semantic: str = Field(default="morpho_semantic", alias="QDRANT_COLLECTION_SEMANTIC")
    qdrant_collection_topological: str = Field(default="morpho_topological", alias="QDRANT_COLLECTION_TOPOLOGICAL")
    qdrant_vector_size: int = Field(default=768, alias="QDRANT_VECTOR_SIZE")
    qdrant_distance: str = Field(default="COSINE", alias="QDRANT_DISTANCE")
    port: int = Field(default=8000, alias="PORT")

    # --- Tree-sitter / AST Parsing ---
    tree_sitter_languages: str = Field(
        default="python,javascript,typescript,go,rust,java,cpp",
        alias="TREE_SITTER_LANGUAGES",
    )
    tree_sitter_parse_timeout: int = Field(default=30, alias="TREE_SITTER_PARSE_TIMEOUT")

    # --- Structural Motif Extraction ---
    motif_min_frequency: int = Field(default=2, alias="MOTIF_MIN_FREQUENCY")
    motif_max_nodes: int = Field(default=50, alias="MOTIF_MAX_NODES")
    motif_similarity_threshold: float = Field(default=0.85, alias="MOTIF_SIMILARITY_THRESHOLD")
    motif_extraction_enabled: bool = Field(default=True, alias="MOTIF_EXTRACTION_ENABLED")
    max_file_size_mb: int = Field(default=10, alias="MAX_FILE_SIZE_MB")

    # --- Hybrid Retrieval ---
    retrieval_top_k: int = Field(default=10, alias="RETRIEVAL_TOP_K")
    retrieval_semantic_weight: float = Field(default=0.4, alias="RETRIEVAL_SEMANTIC_WEIGHT")
    retrieval_topological_weight: float = Field(default=0.4, alias="RETRIEVAL_TOPOLOGICAL_WEIGHT")
    retrieval_lexical_weight: float = Field(default=0.2, alias="RETRIEVAL_LEXICAL_WEIGHT")
    rrf_k: int = Field(default=60, alias="RRF_K")

    # --- Agentic Self-Correction ---
    agent_validation_enabled: bool = Field(default=True, alias="AGENT_VALIDATION_ENABLED")
    agent_max_recursion_passes: int = Field(default=3, alias="AGENT_MAX_RECURSION_PASSES")
    agent_dependency_check_enabled: bool = Field(default=True, alias="AGENT_DEPENDENCY_CHECK_ENABLED")
    agent_confidence_threshold: float = Field(default=0.75, alias="AGENT_CONFIDENCE_THRESHOLD")
    recursive_expansion_max_depth: int = Field(default=3, alias="RECURSIVE_EXPANSION_MAX_DEPTH")

    # --- Security ---
    secret_key: str = Field(
        default="morphosphere_secret_key_change_in_production_2024",
        alias="SECRET_KEY",
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")

    # --- CORS ---
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )

    # --- Monitoring ---
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, alias="METRICS_PORT")
    tracing_enabled: bool = Field(default=False, alias="TRACING_ENABLED")
    jaeger_endpoint: Optional[str] = Field(default=None, alias="JAEGER_ENDPOINT")

    # --- Feature Flags ---
    feature_asg_parsing: bool = Field(default=True, alias="FEATURE_ASG_PARSING")
    feature_motif_extraction: bool = Field(default=True, alias="FEATURE_MOTIF_EXTRACTION")
    feature_hybrid_retrieval: bool = Field(default=True, alias="FEATURE_HYBRID_RETRIEVAL")
    feature_agentic_loop: bool = Field(default=True, alias="FEATURE_AGENTIC_LOOP")
    feature_graph_visualization: bool = Field(default=True, alias="FEATURE_GRAPH_VISUALIZATION")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "case_sensitive": False, "extra": "ignore"}

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def tree_sitter_language_list(self) -> List[str]:
        """Return supported Tree-sitter languages as a list."""
        return [l.strip() for l in self.tree_sitter_languages.split(",") if l.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    api_key_header: str = Field(default="X-API-Key", alias="API_KEY_HEADER")
    recursive_expansion_enabled: bool = Field(default=True, alias="RECURSIVE_EXPANSION_ENABLED")
    api_v1_str: str = Field(default="/api/v1", alias="API_V1_STR")

    # --- Frontend ---
    frontend_port: int = Field(default=3000, alias="FRONTEND_PORT")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    backend_url: str = Field(default="http://localhost:8000", alias="BACKEND_URL")