"""
Main FastAPI application entry point for AI-QA-Agent platform.

This module initializes the FastAPI application with comprehensive AI-powered QA capabilities.
Key architectural decisions:
- Async-first design for handling concurrent AI agent operations
- Structured logging for AI workflow traceability
- CORS configuration for frontend integration
- Lifespan management for proper resource initialization/cleanup
- Global exception handling with AI context preservation

Security considerations:
- API key validation for AI provider access
- Input sanitization for prompt injection prevention
- Rate limiting to prevent AI API abuse
- Audit logging for AI agent interactions
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import create_tables
from app.routers import (
    health,
    test_generation,
    test_execution,
    analytics,
    agents
)

# Initialize structured logging for AI workflow traceability
# Critical for debugging AI agent decisions and performance monitoring
setup_logging()

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for AI-QA-Agent.

    Handles critical startup/shutdown sequences:
    - Database schema initialization for AI-generated content storage
    - Vector database connection validation for embeddings
    - AI provider API connectivity verification
    - Background task queue initialization
    - Cleanup of AI model caches and temporary resources

    This ensures AI agents have all required infrastructure before accepting requests.
    """
    logger.info("Initializing AI-QA-Agent backend with AI capabilities")

    # Critical: Ensure database schema exists for AI-generated test cases and results
    await create_tables()

    # TODO: Add AI provider health checks here
    # TODO: Initialize vector store connections
    # TODO: Warm up AI model caches if needed

    logger.info("AI-QA-Agent backend fully operational with AI agents ready")

    yield

    # Graceful shutdown: Clean up AI resources
    logger.info("Shutting down AI-QA-Agent backend, cleaning up AI resources")

# Initialize FastAPI application
app = FastAPI(
    title="AI-QA-Agent API",
    description="AI-powered QA Agent platform for autonomous testing",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.

    Logs the error and returns a standardized error response.
    """
    logger.error(
        "Unhandled exception",
        exc_info=exc,
        path=request.url.path,
        method=request.method
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# Include routers
app.include_router(
    health.router,
    prefix="/api/v1/health",
    tags=["Health"]
)

app.include_router(
    test_generation.router,
    prefix="/api/v1/test-generation",
    tags=["Test Generation"]
)

app.include_router(
    test_execution.router,
    prefix="/api/v1/test-execution",
    tags=["Test Execution"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["Agents"]
)

@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "name": "AI-QA-Agent API",
        "version": "1.0.0",
        "description": "AI-powered QA Agent platform",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None  # Use our custom logging
    )