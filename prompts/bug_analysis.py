"""
Prompt templates for bug analysis.

Contains structured prompts for analyzing test failures
and providing root cause analysis.
"""

BUG_ANALYSIS_PROMPT = """
You are an expert QA engineer and software debugging specialist. Analyze the following test failure and provide a comprehensive root cause analysis.

FAILURE DATA:
Error Message: {error_message}

Test Logs:
{logs}

Stack Trace:
{stack_trace}

Screenshots: {screenshots}

Test Context: {test_context}

Please provide a detailed analysis following this structure:

1. **ROOT CAUSE IDENTIFICATION**
   - Primary cause of the failure
   - Contributing factors
   - Technical details

2. **IMPACT ASSESSMENT**
   - Severity level (Critical/High/Medium/Low)
   - User impact
   - Business impact

3. **TECHNICAL ANALYSIS**
   - Code/component involved
   - Failure pattern type
   - Environmental factors

4. **RECOMMENDED FIXES**
   - Immediate solutions
   - Long-term improvements
   - Code changes needed

5. **PREVENTION MEASURES**
   - Test improvements
   - Monitoring additions
   - Process changes

6. **CONFIDENCE LEVEL**
   - How certain you are about this analysis
   - Additional information needed

Be specific, actionable, and focus on systemic improvements rather than just quick fixes.
"""

# Additional analysis prompts
PERFORMANCE_ANALYSIS_PROMPT = """
Analyze the following performance test results:

METRICS: {metrics}
THRESHOLDS: {thresholds}
ENVIRONMENT: {environment}

Identify:
1. Performance bottlenecks
2. Scalability issues
3. Resource utilization problems
4. Recommendations for optimization
"""

SECURITY_ANALYSIS_PROMPT = """
Analyze the following for security vulnerabilities:

TEST RESULTS: {test_results}
CODE CHANGES: {code_changes}
DEPENDENCIES: {dependencies}

Identify:
1. Security vulnerabilities
2. Compliance issues
3. Risk assessment
4. Remediation recommendations
"""