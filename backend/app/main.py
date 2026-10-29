"""
MorphoSphere Main Application.

FastAPI application entry point. Configures CORS, middleware,
exception handlers, and includes all API routers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router as api_router
from app.api.dependencies import neo4j_client, qdrant_client
from app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: connect to databases on startup, close on shutdown."""
    logger.info("Starting MorphoSphere backend...")
    neo4j_client.connect()
    qdrant_client.connect()
    logger.info("MorphoSphere backend started successfully.")
    yield
    logger.info("Shutting down MorphoSphere backend...")
    neo4j_client.close()
    qdrant_client.close()
    logger.info("MorphoSphere backend shut down.")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description="Topological & Structural Pattern Engine",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix=settings.api_v1_str)

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "description": "Topological & Structural Pattern Engine",
            "docs": "/docs",
            "health": f"{settings.api_v1_str}/health",
        }

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(exc)},
        )

    return app


app = create_app()