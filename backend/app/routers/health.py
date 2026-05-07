"""
Health check router.

Provides endpoints for monitoring application health,
database connectivity, and system status.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import psutil
import structlog

from app.core.database import get_db, check_db_connection
from app.schemas.health import HealthResponse, SystemInfo

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Basic health check endpoint.

    Returns overall system health status including database connectivity.
    """
    try:
        # Check database connection
        db_healthy = await check_db_connection()

        # Get system information
        system_info = SystemInfo(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent,
            uptime=psutil.boot_time()
        )

        status = "healthy" if db_healthy else "unhealthy"

        response = HealthResponse(
            status=status,
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database=db_healthy,
            system=system_info
        )

        logger.info("Health check performed", status=status, db_healthy=db_healthy)

        return response

    except Exception as e:
        logger.error("Health check failed", error=str(e))

        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database=False,
            system=SystemInfo(
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_usage=0.0,
                uptime=0.0
            )
        )


@router.get("/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """
    Detailed health check with comprehensive system information.

    Includes memory details, disk I/O, network stats, and process information.
    """
    try:
        # Database check
        db_healthy = await check_db_connection()

        # Detailed system metrics
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu = psutil.cpu_times()

        health_data = {
            "status": "healthy" if db_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": {
                    "status": "healthy" if db_healthy else "unhealthy",
                    "type": "postgresql"
                },
                "redis": {
                    "status": "unknown",  # Would need Redis client check
                    "type": "redis"
                }
            },
            "system": {
                "cpu": {
                    "percent": psutil.cpu_percent(interval=0.1),
                    "cores": psutil.cpu_count(),
                    "user": cpu.user,
                    "system": cpu.system,
                    "idle": cpu.idle
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "used": disk.used,
                    "percent": disk.percent
                },
                "network": {
                    "connections": len(psutil.net_connections()),
                    "bytes_sent": psutil.net_io_counters().bytes_sent,
                    "bytes_recv": psutil.net_io_counters().bytes_recv
                }
            },
            "process": {
                "pid": psutil.Process().pid,
                "cpu_percent": psutil.Process().cpu_percent(),
                "memory_percent": psutil.Process().memory_percent(),
                "threads": psutil.Process().num_threads()
            }
        }

        return health_data

    except Exception as e:
        logger.error("Detailed health check failed", error=str(e))

        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }