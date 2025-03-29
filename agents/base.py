from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseAgent(ABC):
    name: str = "base"
    input_keys: List[str] = []
    output_keys: List[str] = []

    def __init__(self, llm=None):
        self.llm = llm

    def __call__(self, state: Dict) -> Dict:
        return self.run(state)

    @abstractmethod
    def run(self, state: Dict) -> Dict:
        """
        입력 state에서 필요한 input_keys를 사용하여
        output_keys를 포함한 새로운 state를 리턴
        """
        pass

    def describe(self) -> Dict:
        return {
            "name": self.name,
            "inputs": self.input_keys,
            "outputs": self.output_keys,
            "uses_llm": self.llm is not None,
        }
