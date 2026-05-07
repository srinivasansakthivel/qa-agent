"""
Test generation router.

Provides endpoints for AI-powered test case generation
from various sources like PRDs, user stories, APIs, etc.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.schemas.test_generation import (
    TestGenerationRequest,
    TestGenerationResponse,
    TestCaseResponse
)
from app.services.test_generation import TestGenerationService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=TestGenerationResponse)
async def generate_tests(
    request: TestGenerationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate test cases using AI agents.

    Supports generation from PRDs, user stories, API specs, screenshots, etc.
    """
    try:
        service = TestGenerationService(db)

        # Generate tests asynchronously
        generation_id = await service.generate_tests_async(request)

        # Add background task for actual generation
        background_tasks.add_task(service.process_generation, generation_id)

        logger.info(
            "Test generation initiated",
            generation_id=generation_id,
            source_type=request.source_type
        )

        return TestGenerationResponse(
            generation_id=generation_id,
            status="processing",
            message="Test generation started successfully"
        )

    except Exception as e:
        logger.error("Test generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")


@router.get("/{generation_id}", response_model=List[TestCaseResponse])
async def get_generated_tests(
    generation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve generated test cases for a generation request.
    """
    try:
        service = TestGenerationService(db)
        test_cases = await service.get_generated_tests(generation_id)

        if not test_cases:
            raise HTTPException(status_code=404, detail="Generation not found or not completed")

        logger.info("Retrieved generated tests", generation_id=generation_id, count=len(test_cases))

        return test_cases

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve generated tests", error=str(e), generation_id=generation_id)
        raise HTTPException(status_code=500, detail="Failed to retrieve test cases")


@router.get("/status/{generation_id}")
async def get_generation_status(generation_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get the status of a test generation request.
    """
    try:
        service = TestGenerationService(db)
        status = await service.get_generation_status(generation_id)

        return {
            "generation_id": generation_id,
            "status": status,
            "timestamp": status.get("timestamp")
        }

    except Exception as e:
        logger.error("Failed to get generation status", error=str(e), generation_id=generation_id)
        raise HTTPException(status_code=500, detail="Failed to get generation status")