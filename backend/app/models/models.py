"""
SQLAlchemy models for the AI-QA-Agent platform.

Defines database tables and relationships for test cases,
executions, results, and analytics.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TestCase(Base):
    """
    Test case model.

    Represents a generated or manual test case with metadata
    and execution history.
    """
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    test_type = Column(String(50), nullable=False)  # api, ui, integration
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    status = Column(String(20), default="draft")  # draft, active, deprecated

    # AI generation metadata
    generated_by = Column(String(100))  # agent name
    generation_prompt = Column(Text)
    confidence_score = Column(Float)

    # Source information
    source_type = Column(String(50))  # prd, user_story, api_spec, screenshot
    source_content = Column(Text)

    # Test steps and expectations
    steps = Column(JSON)  # List of test steps
    expected_results = Column(JSON)  # Expected outcomes

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    executions = relationship("TestExecution", back_populates="test_case")


class TestExecution(Base):
    """
    Test execution model.

    Records individual test runs with results and metadata.
    """
    __tablename__ = "test_executions"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)

    # Execution details
    status = Column(String(20), nullable=False)  # pending, running, passed, failed, error
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float)  # seconds

    # Results
    result_details = Column(JSON)  # Detailed execution results
    error_message = Column(Text)
    screenshots = Column(JSON)  # List of screenshot paths
    logs = Column(Text)

    # Environment
    environment = Column(String(100))  # dev, staging, prod
    browser = Column(String(50))  # chrome, firefox, etc.
    device = Column(String(100))  # desktop, mobile, etc.

    # AI analysis
    ai_analysis = Column(JSON)  # AI-generated analysis of failure
    root_cause = Column(Text)
    suggestions = Column(JSON)  # Improvement suggestions

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    test_case = relationship("TestCase", back_populates="executions")


class TestSuite(Base):
    """
    Test suite model.

    Groups test cases into logical suites for execution.
    """
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Suite configuration
    test_case_ids = Column(JSON)  # List of test case IDs
    execution_config = Column(JSON)  # Parallel execution, timeouts, etc.

    # Status
    status = Column(String(20), default="active")  # active, inactive

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentExecution(Base):
    """
    Agent execution model.

    Tracks AI agent runs and their outcomes.
    """
    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)  # planner, executor, validator, etc.

    # Execution details
    status = Column(String(20), nullable=False)  # pending, running, completed, failed
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    # Input/Output
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)

    # Performance metrics
    tokens_used = Column(Integer)
    cost = Column(Float)
    latency = Column(Float)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsMetric(Base):
    """
    Analytics metrics model.

    Stores aggregated metrics for dashboards and reporting.
    """
    __tablename__ = "analytics_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50), nullable=False)  # counter, gauge, histogram

    # Dimensions
    dimensions = Column(JSON)  # Key-value pairs for filtering/grouping

    # Time window
    timestamp = Column(DateTime, default=datetime.utcnow)
    time_window = Column(String(20))  # hour, day, week, month