from core.registry import register_agent
from agents.code_review import CodeReviewAgent
from agents.test_case_gen import TestCaseGeneratorAgent
from agents.bug_detect import BugDetectionAgent
from agents.report import QAReportAgent

register_agent(TestCaseGeneratorAgent.name, TestCaseGeneratorAgent)
register_agent(CodeReviewAgent.name, CodeReviewAgent)
register_agent(BugDetectionAgent.name, BugDetectionAgent)
register_agent(QAReportAgent.name, QAReportAgent)
