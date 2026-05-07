"""
Pydantic schemas for analytics API.

Defines response models for analytics and reporting.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    """Overall analytics summary."""
    total_tests: int
    total_executions: int
    pass_rate: float
    avg_duration: float
    failure_rate: float
    most_failed_tests: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    generated_at: datetime


class TrendPoint(BaseModel):
    """Data point for trend analysis."""
    date: str
    passed: int
    failed: int
    total: int
    pass_rate: float


class TestTrendsResponse(BaseModel):
    """Test execution trends over time."""
    trends: List[TrendPoint]
    period_days: int
    improvement_rate: Optional[float] = None  # percentage change


class FailurePattern(BaseModel):
    """Failure pattern analysis."""
    pattern_type: str  # timing, environment, test_type, etc.
    description: str
    affected_tests: List[str]
    frequency: int
    impact_score: float


class FailureAnalysisResponse(BaseModel):
    """Failure analysis response."""
    top_failures: List[Dict[str, Any]]
    failure_patterns: List[FailurePattern]
    common_error_messages: List[Dict[str, str]]
    failure_trends: List[TrendPoint]


class CoverageArea(BaseModel):
    """Test coverage for a specific area."""
    area: str
    covered: int
    total: int
    coverage_percentage: float
    risk_level: str  # low, medium, high


class CoverageReport(BaseModel):
    """Test coverage report."""
    overall_coverage: float
    coverage_by_type: List[CoverageArea]
    coverage_by_module: List[CoverageArea]
    uncovered_areas: List[str]
    recommendations: List[str]