from engine.registry import register_agent
from agents.base import BaseAgent

class TestCaseGeneratorAgent(BaseAgent):
    name = "test_case_generator"
    input_keys = ["code"]
    output_keys = ["generated_test"]

    def run(self, state: dict) -> dict:
        code = state.get("code", "")

        if not code:
            raise ValueError("입력 state에 'code' 키가 필요합니다.")

        prompt = (
            "다음 코드에 대해 단위 테스트 케이스를 Python unittest 형식으로 생성해주세요:\n\n"
            f"{code}"
        )

        result = self.llm.generate(prompt) if self.llm else "[생성 실패: LLM 없음]"
        state["generated_test"] = result
        return state

