"""
Test execution router.

Provides endpoints for running test cases, monitoring execution,
and retrieving results.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.schemas.test_execution import (
    TestExecutionRequest,
    TestExecutionResponse,
    TestResultResponse
)
from app.services.test_execution import TestExecutionService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=TestExecutionResponse)
async def execute_tests(
    request: TestExecutionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute test cases.

    Supports running individual tests, test suites, or automated discovery.
    """
    try:
        service = TestExecutionService(db)

        # Start execution asynchronously
        execution_id = await service.execute_tests_async(request)

        # Add background task for actual execution
        background_tasks.add_task(service.process_execution, execution_id)

        logger.info(
            "Test execution initiated",
            execution_id=execution_id,
            test_count=len(request.test_case_ids) if request.test_case_ids else 0
        )

        return TestExecutionResponse(
            execution_id=execution_id,
            status="running",
            message="Test execution started successfully"
        )

    except Exception as e:
        logger.error("Test execution initiation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")


@router.get("/{execution_id}/results", response_model=List[TestResultResponse])
async def get_execution_results(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get results for a test execution.
    """
    try:
        service = TestExecutionService(db)
        results = await service.get_execution_results(execution_id)

        if not results:
            raise HTTPException(status_code=404, detail="Execution not found")

        logger.info("Retrieved execution results", execution_id=execution_id, result_count=len(results))

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve execution results", error=str(e), execution_id=execution_id)
        raise HTTPException(status_code=500, detail="Failed to retrieve results")


@router.get("/{execution_id}/status")
async def get_execution_status(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get the status of a test execution.
    """
    try:
        service = TestExecutionService(db)
        status = await service.get_execution_status(execution_id)

        return {
            "execution_id": execution_id,
            "status": status,
            "progress": status.get("progress", 0),
            "timestamp": status.get("timestamp")
        }

    except Exception as e:
        logger.error("Failed to get execution status", error=str(e), execution_id=execution_id)
        raise HTTPException(status_code=500, detail="Failed to get execution status")


@router.post("/{execution_id}/stop")
async def stop_execution(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Stop a running test execution.
    """
    try:
        service = TestExecutionService(db)
        success = await service.stop_execution(execution_id)

        if success:
            logger.info("Execution stopped", execution_id=execution_id)
            return {"message": "Execution stopped successfully"}
        else:
            raise HTTPException(status_code=404, detail="Execution not found or not running")

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to stop execution", error=str(e), execution_id=execution_id)
        raise HTTPException(status_code=500, detail="Failed to stop execution")