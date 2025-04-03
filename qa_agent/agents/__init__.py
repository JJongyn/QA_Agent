

from .report import QAReportAgent
from .code_review import CodeReviewAgent
from .test_case_gen import TestCaseGeneratorAgent
from .bug_detect import BugDetectionAgent
from .refactor_suggestor import RefactorSuggesterAgent
from .complexity_analyzer import ComplexityAnalyzerAgent

from qa_agent.core.registry import register_agent

ALL_BUILTIN_AGENTS = [
    BugDetectionAgent,
    CodeReviewAgent,
    ComplexityAnalyzerAgent,
    RefactorSuggesterAgent,
    TestCaseGeneratorAgent,
    QAReportAgent
]

for agent_cls in ALL_BUILTIN_AGENTS:
    register_agent(agent_cls.name, agent_cls)
