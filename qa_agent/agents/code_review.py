from qa_agent.core.registry import register_agent
from .base import BaseAgent

class CodeReviewAgent(BaseAgent):
    name = "code_review"
    description = "Analyze code for style, readability, and improvement suggestions."
    input_keys = ["input"]
    output_keys = ["code_review"]
    
    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("input", "")
        
        if not code:
            raise ValueError("입력 state에 'input'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["code_review"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": code})["code_review"]
        
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are a senior software engineer conducting a code review.

        Carefully review the provided Python code and identify:
        - Style issues
        - Design flaws
        - Potential bugs
        - Suggestions for improvement

        Respond in the following JSON format:

        {
        "summary": "Brief summary of the overall review",
        "issues": [
            "Line 14: Variable name `tmp` is too vague",
            "Line 22–30: Deep nesting makes the logic hard to follow"
        ],
        "suggestions": [
            "Use more descriptive variable names",
            "Refactor nested conditionals into helper functions"
        ]
        }

        Code:
        """ + code
        return prompt
        
register_agent(CodeReviewAgent.name, CodeReviewAgent)

