"""
Agents service.

Manages AI agent execution, coordination, and lifecycle.
"""

import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.models.models import AgentExecution
from app.schemas.agents import AgentInfo, AgentStatusResponse, AgentExecutionHistory
from agents.test_generator.agent import TestGeneratorAgent
from agents.bug_analyzer.agent import BugAnalyzerAgent

logger = structlog.get_logger(__name__)


class AgentService:
    """
    Service for managing AI agent operations.

    Handles agent discovery, execution, monitoring, and coordination.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.available_agents = {
            "test_generator": TestGeneratorAgent(),
            "bug_analyzer": BugAnalyzerAgent(),
            # Add more agents as implemented
        }

    async def execute_agent_async(self, request) -> str:
        """
        Initiate asynchronous agent execution.

        Returns an execution ID for tracking.
        """
        # Create execution record
        execution = AgentExecution(
            agent_name=request.agent_name,
            agent_type=self._get_agent_type(request.agent_name),
            status="pending",
            input_data=request.input_data
        )

        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)
        execution_id = str(execution.id)

        logger.info(
            "Agent execution initiated",
            execution_id=execution_id,
            agent_name=request.agent_name
        )

        return execution_id

    async def process_agent_execution(self, execution_id: str):
        """
        Process the actual agent execution.

        This would be called as a background task.
        """
        try:
            # Get execution record
            execution = await self.db.get(AgentExecution, int(execution_id))
            if not execution:
                logger.error("Execution not found", execution_id=execution_id)
                return

            # Update status to running
            execution.status = "running"
            execution.start_time = datetime.utcnow()
            await self.db.commit()

            # Get agent instance
            agent = self.available_agents.get(execution.agent_name)
            if not agent:
                raise ValueError(f"Agent {execution.agent_name} not found")

            # Execute agent
            result = await agent.execute(execution.input_data)

            # Update execution record
            execution.status = "completed" if result.get("status") == "success" else "failed"
            execution.end_time = datetime.utcnow()
            execution.output_data = result
            execution.latency = (execution.end_time - execution.start_time).total_seconds()

            await self.db.commit()

            logger.info(
                "Agent execution completed",
                execution_id=execution_id,
                agent_name=execution.agent_name,
                status=execution.status
            )

        except Exception as e:
            logger.error(
                "Agent execution failed",
                execution_id=execution_id,
                error=str(e)
            )

            # Update execution with error
            if execution:
                execution.status = "failed"
                execution.error_message = str(e)
                execution.end_time = datetime.utcnow()
                await self.db.commit()

    async def get_agent_status(self, execution_id: str) -> AgentStatusResponse:
        """
        Get the status of an agent execution.
        """
        execution = await self.db.get(AgentExecution, int(execution_id))
        if not execution:
            raise ValueError(f"Execution {execution_id} not found")

        return AgentStatusResponse(
            execution_id=execution_id,
            agent_name=execution.agent_name,
            status=execution.status,
            progress=1.0 if execution.status == "completed" else 0.5,  # Mock progress
            start_time=execution.start_time,
            end_time=execution.end_time,
            result=execution.output_data,
            error=execution.error_message
        )

    def list_available_agents(self) -> List[AgentInfo]:
        """
        List all available agents with their capabilities.
        """
        agents = []

        for name, agent in self.available_agents.items():
            agents.append(AgentInfo(
                name=name,
                description=agent.description,
                capabilities=self._get_agent_capabilities(name),
                input_schema={},  # Would be defined per agent
                output_schema={}  # Would be defined per agent
            ))

        return agents

    async def get_agent_history(
        self,
        agent_name: Optional[str] = None,
        limit: int = 50
    ) -> List[AgentExecutionHistory]:
        """
        Get execution history for agents.
        """
        stmt = select(AgentExecution)

        if agent_name:
            stmt = stmt.where(AgentExecution.agent_name == agent_name)

        result = await self.db.execute(
            stmt.order_by(AgentExecution.created_at.desc()).limit(limit)
        )
        executions = result.scalars().all()

        return [
            AgentExecutionHistory(
                execution_id=exec.execution_id if hasattr(exec, 'execution_id') else str(exec.id),
                agent_name=exec.agent_name,
                status=exec.status,
                start_time=exec.start_time or exec.created_at,
                end_time=exec.end_time,
                duration=exec.latency,
                input_summary=str(exec.input_data)[:100] + "..." if exec.input_data else "",
                output_summary=str(exec.output_data)[:100] + "..." if exec.output_data else "",
                error_message=exec.error_message
            )
            for exec in executions
        ]

    async def stop_agent_execution(self, execution_id: str) -> bool:
        """
        Stop a running agent execution.
        """
        execution = await self.db.get(AgentExecution, int(execution_id))
        if not execution or execution.status not in ["pending", "running"]:
            return False

        execution.status = "stopped"
        execution.end_time = datetime.utcnow()
        await self.db.commit()

        logger.info("Agent execution stopped", execution_id=execution_id)
        return True

    def _get_agent_type(self, agent_name: str) -> str:
        """
        Get the type/category of an agent.
        """
        type_mapping = {
            "test_generator": "generator",
            "bug_analyzer": "analyzer",
            "ui_tester": "executor",
            "api_tester": "executor"
        }
        return type_mapping.get(agent_name, "unknown")

    def _get_agent_capabilities(self, agent_name: str) -> List[str]:
        """
        Get the capabilities of an agent.
        """
        capabilities_mapping = {
            "test_generator": ["test_generation", "ai_prompting", "requirements_analysis"],
            "bug_analyzer": ["log_analysis", "screenshot_analysis", "root_cause_analysis"],
            "ui_tester": ["ui_automation", "self_healing_locators", "screenshot_comparison"],
            "api_tester": ["api_testing", "schema_validation", "contract_testing"]
        }
        return capabilities_mapping.get(agent_name, [])
