"""
Pydantic schemas for test execution API.

Defines request/response models for test execution and results.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TestExecutionRequest(BaseModel):
    """Request model for test execution."""
    test_case_ids: Optional[List[int]] = Field(
        default=None,
        description="Specific test case IDs to execute"
    )
    test_suite_id: Optional[int] = Field(
        default=None,
        description="Test suite ID to execute"
    )
    environment: str = Field(
        default="dev",
        description="Execution environment",
        examples=["dev", "staging", "prod"]
    )
    browser: Optional[str] = Field(
        default="chrome",
        description="Browser for UI tests",
        examples=["chrome", "firefox", "safari"]
    )
    parallel: bool = Field(
        default=True,
        description="Whether to run tests in parallel"
    )
    max_concurrent: Optional[int] = Field(
        default=5,
        description="Maximum concurrent test executions"
    )


class TestExecutionResponse(BaseModel):
    """Response model for test execution initiation."""
    execution_id: str
    status: str  # pending, running, completed, failed
    message: str
    estimated_duration: Optional[int] = None  # seconds


class TestStepResult(BaseModel):
    """Result of an individual test step."""
    step_number: int
    status: str  # passed, failed, skipped
    duration: float
    error_message: Optional[str] = None
    screenshot: Optional[str] = None  # screenshot path
    logs: Optional[str] = None


class TestResultResponse(BaseModel):
    """Test execution result model."""
    test_case_id: int
    test_case_title: str
    status: str  # passed, failed, error, skipped
    duration: float
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    step_results: List[TestStepResult] = []
    screenshots: List[str] = []
    logs: Optional[str] = None
    environment: str
    browser: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None  # AI-generated analysis


class ExecutionSummary(BaseModel):
    """Summary of test execution results."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    error: int
    duration: float
    pass_rate: float
    timestamp: datetime