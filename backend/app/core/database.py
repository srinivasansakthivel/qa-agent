"""
Database configuration and session management.

Provides async SQLAlchemy engine and session management
for PostgreSQL database operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """
    Dependency for getting async database session.

    Yields a database session and ensures proper cleanup.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """
    Create all database tables defined in models.

    This function should be called on application startup.
    """
    from app.models import Base

    try:
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(Base.metadata.create_all)

            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise

async def check_db_connection() -> bool:
    """
    Check database connectivity.

    Returns True if connection is successful, False otherwise.
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database connection check failed", error=str(e))
        return False