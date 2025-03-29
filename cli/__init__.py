from engine.registry import register_agent
from agents.code_review import CodeReviewAgent
from agents.test_case_gen import TestCaseGeneratorAgent

register_agent(TestCaseGeneratorAgent.name, TestCaseGeneratorAgent)
register_agent(CodeReviewAgent.name, CodeReviewAgent)
