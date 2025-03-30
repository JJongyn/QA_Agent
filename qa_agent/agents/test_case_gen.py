from qa_agent.core.registry import register_agent
from .base import BaseAgent

class TestCaseGeneratorAgent(BaseAgent):
    name = "test_case_generator"
    description = "Generate Test Cases for the provided code."
    input_keys = ["input"]
    output_keys = ["generated_test"]

    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("input", "")
        
        if not code:
            raise ValueError("입력 state에 'input'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["generated_test"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["generated_test"]
    
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are a test engineer.

        Generate appropriate unit test cases for the following Python function or class.  
        Use the `pytest` framework when possible.

        Respond in the following JSON format:

        {
        "summary": "Description of the test coverage and logic",
        "test_framework": "pytest",
        "test_cases": [
            {
            "name": "test_valid_input",
            "description": "Tests function with valid input",
            "code": "def test_valid_input():\n    assert my_function(2) == 4"
            },
            ...
        ]
        }

        Code:
        """ + code
        return prompt

register_agent(TestCaseGeneratorAgent.name, TestCaseGeneratorAgent)
