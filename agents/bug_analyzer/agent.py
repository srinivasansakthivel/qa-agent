"""
Bug Analyzer Agent.

AI agent responsible for analyzing test failures, logs,
screenshots, and stack traces to provide root cause analysis.
"""

from typing import Dict, Any, List
import structlog

from agents.core.agent_base import BaseAgent
from prompts.bug_analysis import BUG_ANALYSIS_PROMPT

logger = structlog.get_logger(__name__)


class BugAnalyzerAgent(BaseAgent):
    """
    Agent for analyzing bugs and test failures.

    Uses AI to correlate failure data and suggest root causes
    and remediation steps.
    """

    def __init__(self):
        super().__init__(
            name="BugAnalyzerAgent",
            description="Analyzes test failures and provides root cause analysis"
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute bug analysis.

        Args:
            input_data: Contains failure logs, screenshots, stack traces, etc.

        Returns:
            Analysis results with root cause and recommendations
        """
        self._validate_input(input_data, ["failure_data"])

        self._log_execution_start(input_data)

        try:
            analysis = await self.analyze_bug(input_data["failure_data"])

            result = {
                "status": "success",
                "analysis": analysis
            }

            self._log_execution_end(result, 0.0)
            return result

        except Exception as e:
            self.logger.error("Bug analysis execution failed", error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "analysis": {}
            }

    async def analyze_bug(self, failure_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze bug/failure data using AI.

        Args:
            failure_data: Failure logs, screenshots, stack traces, etc.

        Returns:
            Analysis results
        """
        try:
            # Prepare analysis prompt
            prompt = self._build_analysis_prompt(failure_data)

            # Call LLM (mock implementation)
            analysis_text = await self._call_llm(prompt)

            # Parse analysis
            analysis = self._parse_analysis_response(analysis_text)

            # Enhance with additional insights
            analysis.update({
                "confidence_score": self._calculate_confidence(failure_data, analysis),
                "similar_issues": await self._find_similar_issues(failure_data),
                "recommendations": self._generate_recommendations(analysis)
            })

            logger.info("Bug analysis completed", analysis_keys=list(analysis.keys()))

            return analysis

        except Exception as e:
            logger.error("Bug analysis failed", error=str(e))
            raise

    def _build_analysis_prompt(self, failure_data: Dict[str, Any]) -> str:
        """
        Build the analysis prompt from failure data.
        """
        logs = failure_data.get("logs", "")
        screenshots = failure_data.get("screenshots", [])
        stack_trace = failure_data.get("stack_trace", "")
        error_message = failure_data.get("error_message", "")
        test_context = failure_data.get("test_context", {})

        return BUG_ANALYSIS_PROMPT.format(
            error_message=error_message,
            logs=logs[:2000],  # Truncate for token limits
            stack_trace=stack_trace,
            screenshots=f"{len(screenshots)} screenshots available",
            test_context=str(test_context)
        )

    async def _call_llm(self, prompt: str) -> str:
        """
        Call LLM for bug analysis.
        """
        # Mock LLM response
        return """
        ROOT CAUSE ANALYSIS:
        The failure appears to be caused by a timing issue in the UI where the login button becomes clickable before the form validation completes.

        TECHNICAL DETAILS:
        - Error: "Element not interactable"
        - Stack trace shows Selenium waiting timeout
        - Screenshot analysis reveals button is visible but disabled

        SEVERITY: High
        IMPACT: Blocks user authentication flow

        RECOMMENDED FIXES:
        1. Add explicit wait for button to be enabled
        2. Implement retry logic with exponential backoff
        3. Add form validation state checking

        PREVENTION:
        - Implement self-healing locators
        - Add visual regression testing
        - Increase test stability checks
        """

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM analysis response.
        """
        # Simple parsing - in production would use more sophisticated parsing
        return {
            "root_cause": "Timing issue with UI element interaction",
            "severity": "High",
            "impact": "Blocks critical user flow",
            "technical_details": {
                "error_type": "Element interaction timeout",
                "component": "Login form",
                "failure_pattern": "Race condition"
            },
            "recommended_fixes": [
                "Add explicit wait conditions",
                "Implement retry mechanism",
                "Add form state validation"
            ],
            "prevention_measures": [
                "Self-healing locators",
                "Visual regression tests",
                "Stability monitoring"
            ]
        }

    def _calculate_confidence(self, failure_data: Dict[str, Any], analysis: Dict[str, Any]) -> float:
        """
        Calculate confidence score for the analysis.
        """
        # Simple confidence calculation based on data completeness
        score = 0.5  # Base score

        if failure_data.get("logs"):
            score += 0.1
        if failure_data.get("stack_trace"):
            score += 0.15
        if failure_data.get("screenshots"):
            score += 0.1
        if failure_data.get("error_message"):
            score += 0.1

        # Analysis quality factors
        if analysis.get("technical_details"):
            score += 0.05

        return min(score, 1.0)

    async def _find_similar_issues(self, failure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find similar historical issues.
        """
        # Mock similar issues - in production would search vector DB
        return [
            {
                "issue_id": "BUG-123",
                "title": "Login button timing issue",
                "similarity_score": 0.85,
                "resolution": "Added wait condition",
                "date": "2024-01-15"
            }
        ]

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate additional recommendations based on analysis.
        """
        recommendations = analysis.get("recommended_fixes", [])

        # Add general recommendations
        recommendations.extend([
            "Add comprehensive error logging",
            "Implement circuit breaker pattern",
            "Create automated retry mechanisms",
            "Add performance monitoring"
        ])

        return list(set(recommendations))  # Remove duplicates