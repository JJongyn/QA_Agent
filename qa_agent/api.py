from .core.auto_selector import run_general_qa
from .core.registry import get_agent, register_agent
from .core.workflow import WorkflowEngine
from .llm.chatgpt import ChatGPTLLM
from .utils.util import *

def run_auto_qa(query: str, input: str, model: str, model_type: str, use_summary: bool) -> dict:
    llm = load_llm(model=model, model_type=model_type)
    input = resolve_input(input)
    result = run_general_qa(query=query, user_input={"input": input}, llm=llm, include_report=True)
    return result.get("qa_report", "[요약 리포트 없음]") if use_summary else result

def run_workflow_qa(input: str, model: str, model_type: str, yaml_path: str) -> dict:
    llm = load_llm(model=model, model_type=model_type)
    engine = WorkflowEngine()
    engine.load_from_yaml(yaml_path, llm=llm)
    result = engine.run({"input": input})
    return result

def run_single_qa(input: str, agent_name:str, model: str, model_type: str) -> dict:
    llm = load_llm(model=model, model_type=model_type)
    AgentClass = get_agent(agent_name)
    agent = AgentClass(llm=llm)
    result = agent({"input": input})
    return result

__all__ = [
    "run_auto_qa",
    "run_workflow_qa",
    "run_single_qa",
    "get_agent",
    "register_agent"
]
