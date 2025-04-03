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
        당신은 시니어 소프트웨어 엔지니어입니다.  
        아래에 주어진 Python 코드를 읽고 다음 항목에 대한 리뷰를 작성해주세요:

        - 코드 스타일 및 포매팅
        - 가독성과 유지보수성
        - 버그 가능성 또는 논리적 문제
        - 개선을 위한 제안

        객관적이고 명확하게, 그리고 개발자에게 도움이 되는 방식으로 작성해주세요.  
        응답은 마크다운 형식으로 깔끔하게 정리해주세요.

        ### 🔍 리뷰 대상 코드:
        ```Code
        {code}
        """ 
        return prompt
        


