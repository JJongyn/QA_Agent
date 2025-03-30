from qa_agent.core.registry import register_agent
from .base import BaseAgent

class QAReportAgent(BaseAgent):
    name = "qa_report_generator"
    description = "Generate a markdown report summarizing all string-type outputs in the process."
    input_keys = []  # 모든 state를 읽음
    output_keys = ["qa_report"]

    # def run(self, state: dict) -> dict:
    #     sections = []

    #     for key, value in state.items():
    #         if key in self.output_keys:
    #             continue
    #         if isinstance(value, str) and value.strip():
    #             sections.append(f"## {key}\n{value.strip()}\n")

    #     report = "# 🧪 QA 종합 리포트\n\n" + "\n".join(sections)
    #     state["qa_report"] = report
    #     return state

    def run(self, state:dict) -> dict:
        sections = []

        for key, value in state.items():
            if key in self.output_keys:
                continue
            if isinstance(value, str) and value.strip():
                sections.append(f"## {key}\n{value.strip()}\n")
        
        prompt = self.build_prompt(sections)
        review_result = self.llm.generate(prompt) if self.llm else "[리뷰 결과 없음]: LLM을 등록해주세요."
        
        state["qa_report"] = review_result
        return state
    
    def run_with_input(self, code:str) -> str:
        # 일반용
        return self.run({"input": input})["qa_report"]
    
    def build_prompt(self, code: str) -> str:
        prompt = """
        You are a QA manager writing a final report.

        Summarize the results of multiple QA agents (code review, bug detection, testing, etc.)  
        into a readable Markdown report.

        Input may include:
        - `code_review`
        - `bugs_found`
        - `generated_test`
        - `refactor_suggestion`
        - etc.

        Respond in the following JSON format:

        {
        "summary_markdown": "# QA Summary\n\n## Code Review\n...\n\n## Bugs\n...\n"
        }
        
        Input:
        """ + code
        return prompt

register_agent(QAReportAgent.name, QAReportAgent)
        
