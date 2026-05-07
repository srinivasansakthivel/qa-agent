"""
Pydantic schemas for agents API.

Defines request/response models for AI agent interactions.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class AgentExecutionRequest(BaseModel):
    """Request model for agent execution."""
    agent_name: str
    input_data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None  # Additional execution options


class AgentExecutionResponse(BaseModel):
    """Response model for agent execution initiation."""
    execution_id: str
    status: str  # pending, running, completed, failed
    message: str
    estimated_duration: Optional[int] = None  # seconds


class AgentInfo(BaseModel):
    """Information about an available agent."""
    name: str
    description: str
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class AgentListResponse(BaseModel):
    """Response model for listing available agents."""
    agents: List[AgentInfo]
    total_count: int


class AgentStatusResponse(BaseModel):
    """Response model for agent execution status."""
    execution_id: str
    agent_name: str
    status: str
    progress: Optional[float] = None  # 0.0 to 1.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentExecutionHistory(BaseModel):
    """Agent execution history entry."""
    execution_id: str
    agent_name: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    input_summary: str
    output_summary: Optional[str] = None
    error_message: Optional[str] = None