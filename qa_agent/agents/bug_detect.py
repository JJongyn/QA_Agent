from .base import BaseAgent

class BugDetectionAgent(BaseAgent):
    name = "bug_detection"
    description = "Identify potential bugs and exception-prone areas in the code."
    input_keys = ["input"]
    output_keys = ["bugs_found"]
    
    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("input", "")
        
        if not code:
            raise ValueError("입력 state에 'input'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["bugs_found"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["bugs_found"]
        
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are a software QA expert.

        Analyze the given Python code and detect:
        - Potential bugs or runtime errors
        - Logical flaws or incorrect behavior
        - Edge cases that may cause failure

        Respond in the following JSON format:

        {
        "summary": "High-level overview of bug findings",
        "bugs": [
            "Line 12: Possible division by zero",
            "Line 35: Variable `count` might be undefined"
        ],
        "recommendations": [
            "Add a check before dividing by variable `x`",
            "Initialize `count` with a default value"
        ]
        }
        Code: {code}
        """ 
        return prompt
        


