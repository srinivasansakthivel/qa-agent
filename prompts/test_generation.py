"""
Advanced prompt engineering templates for AI-powered test case generation.

This module contains carefully crafted prompts designed for optimal LLM performance
in test case generation tasks. Key prompt engineering techniques employed:

PROMPT ENGINEERING STRATEGIES:
1. Role Definition: Clear expert role assignment for domain-specific knowledge
2. Structured Output: JSON schema enforcement for parseable results
3. Chain-of-Thought: Step-by-step reasoning for complex test scenarios
4. Few-Shot Learning: Quality examples for consistent output patterns
5. Constraint Specification: Clear boundaries and requirements
6. Context Window Optimization: Efficient token usage for cost control

AI SAFETY MEASURES:
- Input sanitization to prevent prompt injection
- Output validation against expected schemas
- Confidence scoring for generated content
- Fallback mechanisms for parsing failures

PERFORMANCE OPTIMIZATIONS:
- Template-based prompt construction for reusability
- Parameterized inputs for dynamic content
- Token counting and cost estimation
- Response caching for similar inputs

QUALITY ASSURANCE:
- Structured validation of generated test cases
- Completeness checking against requirements
- Consistency validation across test types
- Automated review triggers for low-confidence outputs

SCALABILITY FEATURES:
- Batch processing capabilities for large inputs
- Streaming responses for real-time generation
- Memory-efficient prompt construction
- Configurable complexity levels
"""

TEST_GENERATION_PROMPT = """
You are a senior QA engineering expert with 15+ years of experience in test automation,
quality assurance methodologies, and software testing best practices. Your expertise includes
functional testing, security testing, accessibility testing, and performance testing.

SOURCE TYPE: {source_type}
SOURCE CONTENT:
{source_content}

REQUIRED TEST TYPES: {test_types}

GENERATE COMPREHENSIVE TEST CASES using the following expert methodology:

1. **REQUIREMENTS ANALYSIS**:
   - Identify all functional requirements and user workflows
   - Extract business rules and validation logic
   - Determine integration points and external dependencies
   - Assess security and compliance requirements

2. **TEST CASE ARCHITECTURE**:
   - title: Action-oriented, descriptive title following "Should [expected behavior]"
   - description: Detailed explanation of test purpose and scope
   - test_type: {test_types} (select most appropriate)
   - priority: critical/high/medium/low based on business impact and risk
   - steps: Sequential, atomic actions with clear success criteria
   - expected_results: Measurable outcomes with pass/fail definitions
   - confidence_score: 0.0-1.0 based on requirements clarity and test feasibility

3. **TEST TYPE SPECIFICS**:
   - **positive**: Core functionality validation with valid inputs
   - **negative**: Error handling and invalid input validation
   - **edge**: Boundary conditions, limits, and unusual valid scenarios
   - **security**: Authentication, authorization, injection, and data protection
   - **accessibility**: WCAG compliance, keyboard navigation, screen readers

4. **STEP PRECISION**:
   {{
     "step_number": 1,
     "action": "Specific, executable action (e.g., 'Enter username 'test@example.com' in email field')",
     "expected_result": "Observable, verifiable outcome (e.g., 'Email field accepts input and shows valid format')",
     "data": {{"key": "value"}} // Test data with realistic values
   }}

5. **QUALITY CRITERIA**:
   - Atomic: Each test validates one specific behavior
   - Independent: No dependencies on other test execution order
   - Traceable: Clear link to requirements or user stories
   - Automated: Suitable for automated execution
   - Maintainable: Clear, readable test logic

6. **COVERAGE CONSIDERATIONS**:
   - Happy path and error scenarios
   - Data validation and business rules
   - Integration points and APIs
   - User experience and accessibility
   - Security and performance boundaries

Generate 3-5 high-quality test cases that provide comprehensive coverage of the specified functionality.
Each test case must be immediately executable and include all necessary test data and assertions.

Return results as valid JSON array with consistent structure and realistic test data.
Return the response as a valid JSON array of test case objects.
"""

# Additional prompt templates can be added here
ANALYSIS_PROMPT = """
Analyze the following test execution results and provide insights:

TEST RESULTS: {test_results}
EXECUTION CONTEXT: {context}

Please provide:
1. Root cause analysis
2. Failure patterns
3. Recommendations for fixes
4. Prevention strategies
"""

BUG_REPORT_PROMPT = """
Generate a comprehensive bug report from the following information:

ISSUE DETAILS: {issue_details}
REPRODUCTION STEPS: {reproduction_steps}
ENVIRONMENT: {environment}

Create a Jira-ready bug report with:
- Summary
- Description
- Steps to reproduce
- Expected vs actual results
- Environment details
- Severity assessment
"""
