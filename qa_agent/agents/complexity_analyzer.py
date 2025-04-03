from .base import BaseAgent

class ComplexityAnalyzerAgent(BaseAgent):
    name = "complexity_analyzer"
    description = "코드 복잡도, 구조 개선, 함수 길이 등을 분석합니다."
    input_keys = ["input"]
    output_keys = ["complexity_feedback"]

    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("input", "")
        
        if not code:
            raise ValueError("입력 state에 'input'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["complexity_feedback"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["complexity_feedback"]
    
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are a software analysis tool.

        Evaluate the complexity of the given Python code based on:
        - Function length and nesting
        - Cyclomatic complexity
        - Overall readability

        Respond in the following JSON format:

        {
        "summary": "Short description of the complexity level",
        "complexity_score": "High",  // or "Medium", "Low"
        "reasons": [
            "Multiple nested loops and conditionals",
            "Function exceeds 50 lines"
        ],
        "improvement_suggestions": [
            "Split long function into smaller sub-functions",
            "Reduce nesting using guard clauses"
        ]
        }

        Code: {code}
        """ 
        return prompt


