from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        LLM에 prompt를 보내고 결과 텍스트를 리턴
        """
        pass
