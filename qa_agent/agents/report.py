from .base import BaseAgent

class QAReportAgent(BaseAgent):
    name = "qa_report_generator"
    description = "Generate a report summarizing all string-type outputs in the process."
    input_keys = []  # 모든 state를 읽음
    output_keys = ["qa_report"]
   
    def run(self, state:dict) -> dict:
        q = state.get(state['query'], 'None')
        
        sections = []
        for key, value in state.items():
            if key in self.output_keys:
                continue
            if isinstance(value, str) and value.strip():
                # sections.append(f"## {key}\n{value.strip()}\n")
                sections.append(f"## {key.replace('_', ' ').title()}\n{value.strip()}\n")

        qa_contents = "\n".join(sections)
        # print(qa_contents)
        
        # prompt = self.build_prompt(qa_contents, q)
        # review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        # state["qa_report"] = review_result
        return qa_contents
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["qa_report"]
    
    def build_prompt(self, code: str, user_query: str) -> str:
        prompt = """
        당신은 아래에 입력되는 값에 대하여 사용자가 읽기 좋은 형태로 바꿔주세요.
        
        ## 주의할 점
        1. 내용을 수정하거나 빼서는 안됩니다.
        
        입력:
        {code}
        """ 
        return prompt


        
