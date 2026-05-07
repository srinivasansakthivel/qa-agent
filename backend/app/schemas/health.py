"""
Pydantic schemas for health check responses.

Defines the structure of health check API responses.
"""

from datetime import datetime
from pydantic import BaseModel


class SystemInfo(BaseModel):
    """System resource information."""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    uptime: float


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str  # healthy, unhealthy, degraded
    timestamp: datetime
    version: str
    database: bool
    system: SystemInfo