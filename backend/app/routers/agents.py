"""
Agents router.

Provides endpoints for interacting with AI agents,
monitoring their status, and managing agent operations.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.schemas.agents import (
    AgentExecutionRequest,
    AgentExecutionResponse,
    AgentStatusResponse,
    AgentListResponse
)
from app.services.agents import AgentService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/execute", response_model=AgentExecutionResponse)
async def execute_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute an AI agent with the given input.
    """
    try:
        service = AgentService(db)

        # Start agent execution asynchronously
        execution_id = await service.execute_agent_async(request)

        # Add background task for actual execution
        background_tasks.add_task(service.process_agent_execution, execution_id)

        logger.info(
            "Agent execution initiated",
            execution_id=execution_id,
            agent_name=request.agent_name
        )

        return AgentExecutionResponse(
            execution_id=execution_id,
            status="running",
            message=f"Agent {request.agent_name} execution started"
        )

    except Exception as e:
        logger.error("Agent execution initiation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@router.get("/status/{execution_id}", response_model=AgentStatusResponse)
async def get_agent_status(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get the status of an agent execution.
    """
    try:
        service = AgentService(db)
        status = await service.get_agent_status(execution_id)

        return status

    except Exception as e:
        logger.error("Failed to get agent status", error=str(e), execution_id=execution_id)
        raise HTTPException(status_code=500, detail="Failed to get agent status")


@router.get("/list", response_model=AgentListResponse)
async def list_agents():
    """
    List all available agents.
    """
    try:
        service = AgentService(None)  # No DB needed for listing
        agents = service.list_available_agents()

        return AgentListResponse(agents=agents)

    except Exception as e:
        logger.error("Failed to list agents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list agents")


@router.get("/history")
async def get_agent_history(
    agent_name: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get execution history for agents.
    """
    try:
        service = AgentService(db)
        history = await service.get_agent_history(agent_name, limit)

        return {"history": history, "count": len(history)}

    except Exception as e:
        logger.error("Failed to get agent history", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get agent history")


@router.post("/stop/{execution_id}")
async def stop_agent_execution(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Stop a running agent execution.
    """
    try:
        service = AgentService(db)
        success = await service.stop_agent_execution(execution_id)

        if success:
            logger.info("Agent execution stopped", execution_id=execution_id)
            return {"message": "Agent execution stopped successfully"}
        else:
            raise HTTPException(status_code=404, detail="Agent execution not found or not running")

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to stop agent execution", error=str(e), execution_id=execution_id)
        raise HTTPException(status_code=500, detail="Failed to stop agent execution")