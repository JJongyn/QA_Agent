from engine.registry import register_agent
from agents.base import BaseAgent

class CodeReviewAgent(BaseAgent):
    name = "code_review"
    input_keys = ["code"]
    output_keys = ["code_review"]
    
    def run(self, state:dict) -> dict:
        # langraph용
        code = state.get("code", "")
        
        if not code:
            raise ValueError("입력 state에 'code'키가 없습니다.")
        
        prompt = self.build_prompt(code)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["code_review"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"code": code})["code_review"]
        
    def build_prompt(self, code: str) -> str:
        return (
            "다음 코드를 리뷰해주세요. 문제점, 개선점, 버그 가능성 등을 포함해 설명해주세요:\n\n"
            f"{code}"
        )
        
register_agent(CodeReviewAgent.name, CodeReviewAgent)

