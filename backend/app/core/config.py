"""
AI-QA-Agent configuration management with comprehensive AI settings.

This module provides type-safe configuration management using Pydantic,
specifically designed for AI-powered QA applications. Key considerations:

AI-Specific Configuration:
- Multiple LLM provider support for redundancy and cost optimization
- Model selection based on task complexity (GPT-4 for reasoning, GPT-3.5 for speed)
- Embedding model configuration for semantic search capabilities
- Token limits and rate limiting to control AI API costs

Security Considerations:
- API keys loaded from environment variables only (never hardcoded)
- Separate keys for different AI providers to enable provider failover
- No sensitive AI prompts or keys exposed in logs or responses

Performance Optimization:
- Configurable model selection based on task requirements
- Caching settings to reduce redundant AI calls
- Rate limiting to prevent API quota exhaustion
- Connection pooling for database and AI provider APIs

Scalability Features:
- Environment-specific configurations (dev/staging/prod)
- Dynamic model selection based on load and cost constraints
- Vector database abstraction for future scaling needs
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Comprehensive application settings for AI-QA-Agent.

    All AI-related settings are configurable to enable:
    - Cost optimization across different AI providers
    - Performance tuning based on workload characteristics
    - Security hardening for production deployments
    - Scalability adjustments for different environments

    Environment Variable Pattern:
    - AI_QA_AGENT_<SETTING_NAME> for global override
    - Individual provider keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
    """

    # Application Metadata
    APP_NAME: str = "AI-QA-Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(
        default=False,
        env="DEBUG",
        description="Enable debug mode (WARNING: May expose sensitive AI data in logs)"
    )

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins for frontend integration"
    )

    # Database Configuration
    # Uses asyncpg for high-performance async database operations
    # Critical for handling concurrent AI agent requests
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/qa_agent",
        env="DATABASE_URL",
        description="PostgreSQL connection string with async support"
    )

    # Redis Configuration
    # Used for caching AI responses and background task queuing
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL",
        description="Redis connection for caching and task queuing"
    )

    # Primary AI Provider - OpenAI
    # GPT-4-turbo-preview selected for optimal reasoning capabilities
    # while maintaining cost efficiency
    OPENAI_API_KEY: str = Field(
        ...,
        env="OPENAI_API_KEY",
        description="OpenAI API key - REQUIRED for AI functionality"
    )
    OPENAI_MODEL: str = Field(
        default="gpt-4-turbo-preview",
        env="OPENAI_MODEL",
        description="Primary LLM model for complex reasoning tasks"
    )
    OPENAI_EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-small",
        env="OPENAI_EMBEDDING_MODEL",
        description="Embedding model for semantic search and similarity"
    )

    # Alternative LLM Providers for Redundancy and Cost Optimization
    # Enables automatic failover and provider selection based on cost/performance
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        env="ANTHROPIC_API_KEY",
        description="Anthropic Claude API key for alternative AI provider"
    )
    COHERE_API_KEY: Optional[str] = Field(
        default=None,
        env="COHERE_API_KEY",
        description="Cohere API key for embedding and generation tasks"
    )

    # Vector Database Configuration
    # Supports multiple backends for scalability and cost optimization
    VECTOR_DB_TYPE: str = Field(
        default="chromadb",
        env="VECTOR_DB_TYPE",
        description="Vector database type: chromadb, faiss, pinecone, etc."
    )
    CHROMA_DB_PATH: str = Field(
        default="./data/chromadb",
        env="CHROMA_DB_PATH",
        description="Local ChromaDB storage path"
    )
    CHROMA_DB_PATH: str = "./data/chromadb"

    # Playwright
    PLAYWRIGHT_BROWSERS_PATH: Optional[str] = None
    PLAYWRIGHT_HEADLESS: bool = True

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Observability
    OTLP_ENDPOINT: Optional[str] = Field(default=None, env="OTLP_ENDPOINT")
    PROMETHEUS_PORT: int = 9090

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Caching
    CACHE_TTL: int = 3600  # 1 hour
    LLM_CACHE_SIZE: int = 1000

    # Test Execution
    MAX_CONCURRENT_TESTS: int = 10
    TEST_TIMEOUT: int = 300  # 5 minutes

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()