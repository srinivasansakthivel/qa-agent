"""
Analytics router.

Provides endpoints for test analytics, dashboards,
and reporting features.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.schemas.analytics import (
    AnalyticsSummary,
    TestTrendsResponse,
    FailureAnalysisResponse,
    CoverageReport
)
from app.services.analytics import AnalyticsService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = Query(30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall analytics summary.
    """
    try:
        service = AnalyticsService(db)
        summary = await service.get_summary(days)

        logger.info("Analytics summary retrieved", days=days)

        return summary

    except Exception as e:
        logger.error("Failed to get analytics summary", error=str(e))
        raise


@router.get("/trends", response_model=TestTrendsResponse)
async def get_test_trends(
    days: int = Query(30, description="Number of days for trend analysis"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get test execution trends over time.
    """
    try:
        service = AnalyticsService(db)
        trends = await service.get_trends(days)

        return trends

    except Exception as e:
        logger.error("Failed to get test trends", error=str(e))
        raise


@router.get("/failures", response_model=FailureAnalysisResponse)
async def get_failure_analysis(
    days: int = Query(7, description="Number of days to analyze failures"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get failure analysis and patterns.
    """
    try:
        service = AnalyticsService(db)
        analysis = await service.get_failure_analysis(days)

        return analysis

    except Exception as e:
        logger.error("Failed to get failure analysis", error=str(e))
        raise


@router.get("/coverage", response_model=CoverageReport)
async def get_coverage_report(
    db: AsyncSession = Depends(get_db)
):
    """
    Get test coverage report.
    """
    try:
        service = AnalyticsService(db)
        coverage = await service.get_coverage_report()

        return coverage

    except Exception as e:
        logger.error("Failed to get coverage report", error=str(e))
        raise


@router.get("/flaky-tests")
async def get_flaky_tests(
    threshold: float = Query(0.8, description="Failure rate threshold for flaky detection"),
    days: int = Query(30, description="Analysis period in days"),
    db: AsyncSession = Depends(get_db)
):
    """
    Identify potentially flaky tests based on execution patterns.
    """
    try:
        service = AnalyticsService(db)
        flaky_tests = await service.detect_flaky_tests(threshold, days)

        return {
            "flaky_tests": flaky_tests,
            "threshold": threshold,
            "analysis_period_days": days
        }

    except Exception as e:
        logger.error("Failed to detect flaky tests", error=str(e))
        raise