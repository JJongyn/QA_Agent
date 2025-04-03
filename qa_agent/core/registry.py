from typing import Dict, Type
from qa_agent.agents.base import BaseAgent

_AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {}

def register_agent(name:str, agent_cls:Type[BaseAgent]):
    if not issubclass(agent_cls, BaseAgent):
        raise ValueError(f"{name}는 BaseAgent를 상속해야 합니다.")
    _AGENT_REGISTRY[name] = agent_cls

def get_agent() -> Dict[str, Type[BaseAgent]]:
    return _AGENT_REGISTRY.copy()

def find_agent(name:str) -> Type[BaseAgent]:
    if name not in _AGENT_REGISTRY:
        raise ValueError(f"{name}라는 Agent가 등록되어 있지 않습니다.")
    return _AGENT_REGISTRY[name]


