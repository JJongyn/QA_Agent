from .base import BaseAgent

class RefactorSuggesterAgent(BaseAgent):
    name = "refactor_suggester"
    description = "코드의 리팩토링 가능한 부분을 찾아 제안합니다."
    input_keys = ["input"]
    output_keys = ["refactor_suggestion"]

    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("input", "")
        
        if not code:
            raise ValueError("입력 state에 'input'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["refactor_suggestion"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["refactor_suggestion"]
    
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are an expert in clean code and software refactoring.

        Analyze the given code and suggest improvements based on:
        - Redundant or duplicated logic
        - Long or deeply nested functions
        - Naming conventions
        - Performance and maintainability

        Respond in the following JSON format:

        {
        "summary": "Overall evaluation of code structure",
        "refactor_points": [
            "Extract duplicated code in lines 10–20 into a helper function",
            "Rename variable `x` to `user_count`"
        ],
        "explanation": "Refactoring improves readability and reduces maintenance cost"
        }

        Code: {code}
        """ 
        return prompt


