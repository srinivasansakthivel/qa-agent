"""
Pydantic schemas for test generation API.

Defines request/response models for AI-powered test case generation.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TestGenerationRequest(BaseModel):
    """Request model for test case generation."""
    source_type: str = Field(
        ...,
        description="Type of source material",
        examples=["prd", "user_story", "api_spec", "screenshot", "swagger"]
    )
    source_content: str = Field(
        ...,
        description="The actual source content to generate tests from"
    )
    test_types: List[str] = Field(
        default=["positive", "negative", "edge"],
        description="Types of tests to generate",
        examples=[["positive", "negative", "edge", "security", "accessibility"]]
    )
    priority: Optional[str] = Field(
        default="medium",
        description="Test priority level",
        examples=["low", "medium", "high", "critical"]
    )
    additional_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for generation"
    )


class TestGenerationResponse(BaseModel):
    """Response model for test generation initiation."""
    generation_id: str
    status: str  # processing, completed, failed
    message: str
    estimated_time: Optional[int] = None  # seconds


class TestStep(BaseModel):
    """Individual test step model."""
    step_number: int
    action: str
    expected_result: str
    data: Optional[Dict[str, Any]] = None


class TestCaseResponse(BaseModel):
    """Generated test case response model."""
    id: Optional[int] = None
    title: str
    description: str
    test_type: str
    priority: str
    steps: List[TestStep]
    expected_results: Dict[str, Any]
    generated_by: str
    confidence_score: Optional[float] = None
    tags: List[str] = []
    created_at: Optional[datetime] = None