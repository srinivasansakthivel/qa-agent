"""
Test generation service.

Handles AI-powered test case generation using various agents
and prompt templates.
"""

from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.models.models import TestCase
from app.schemas.test_generation import TestCaseResponse, TestStep
from agents.test_generator.agent import TestGeneratorAgent

logger = structlog.get_logger(__name__)


class TestGenerationService:
    """
    Service for generating test cases using AI agents.

    Orchestrates the test generation process from various sources
    and manages the generation lifecycle.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent = TestGeneratorAgent()

    async def generate_tests_async(self, request) -> str:
        """
        Initiate asynchronous test generation.

        Returns a generation ID for tracking progress.
        """
        logger.info(
            "Initiating test generation",
            source_type=request.source_type
        )

        test_cases = await self.agent.generate_tests(request.model_dump())

        first_test_case_id = None
        for test_case_data in test_cases:
            test_case = TestCase(
                title=test_case_data["title"],
                description=test_case_data["description"],
                test_type=test_case_data["test_type"],
                priority=test_case_data.get("priority", request.priority or "medium"),
                generated_by="TestGeneratorAgent",
                source_type=request.source_type,
                source_content=request.source_content,
                steps=test_case_data.get("steps", []),
                expected_results=test_case_data.get("expected_results", {}),
                confidence_score=test_case_data.get("confidence_score", 0.8),
            )

            self.db.add(test_case)
            await self.db.flush()
            if first_test_case_id is None:
                first_test_case_id = test_case.id

        await self.db.commit()

        return str(first_test_case_id or "0")

    async def process_generation(self, generation_id: str):
        """
        Process the actual test generation.

        This would be called as a background task.
        """
        try:
            logger.info(
                "Test generation already completed synchronously",
                generation_id=generation_id,
            )

        except Exception as e:
            logger.error(
                "Test generation failed",
                generation_id=generation_id,
                error=str(e)
            )
            await self.db.rollback()

    async def get_generated_tests(self, generation_id: str) -> List[TestCaseResponse]:
        """
        Retrieve generated test cases for a generation request.
        """
        # In production, this would filter by generation_id
        # For now, return all test cases
        stmt = select(TestCase).order_by(TestCase.created_at.desc()).limit(50)
        result = await self.db.execute(stmt)
        test_cases = result.scalars().all()

        if generation_id.isdigit() and generation_id != "0":
            requested_id = int(generation_id)
            matching = [tc for tc in test_cases if tc.id == requested_id]
            test_cases = matching or test_cases

        return [
            TestCaseResponse(
                id=tc.id,
                title=tc.title,
                description=tc.description,
                test_type=tc.test_type,
                priority=tc.priority,
                steps=[TestStep(**step) for step in tc.steps] if tc.steps else [],
                expected_results=tc.expected_results or {},
                generated_by=tc.generated_by,
                confidence_score=tc.confidence_score,
                created_at=tc.created_at
            )
            for tc in test_cases
        ]

    async def get_generation_status(self, generation_id: str) -> Dict[str, Any]:
        """
        Get the status of a test generation request.
        """
        # Mock status - in production would check cache/queue
        return {
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
            "progress": 100
        }
