import os

from qa_agent import run_auto_qa, run_workflow_qa, run_single_qa
from qa_agent.utils import *
result = run_auto_qa(
    query="이 코드에 대해 리뷰하고 text case 생성해줘",
    input="def add(a, b): return a + b",
    model="chatgpt",
    model_type="gpt-3.5-turbo",
    use_summary=False
)

print(result)
# result = run_workflow_qa(
#     input="def is_even(n): return n % 2 == 0",
#     model="chatgpt",
#     model_type="gpt-3.5-turbo",
#     yaml_path="./review_and_test.yaml"
# )

save_report_as_pdf(result)


# from qa_agent import run_single_qa

# result = run_single_qa(
#     input="def multiply(a, b): return a * b",
#     agent_name="code_review",
#     model="chatgpt",
#     model_type="gpt-3.5-turbo"
# )

# print("📋 코드 리뷰 결과:\n", result.get("code_review"))


# =====통과 ======#
# from qa_agent.utils.util import create_prompt_agent, save_prompt_agent, load_prompt_aget

# 실행 #### 동적으로 prompt agent 생성하기
# create_prompt_agent(
#     name="simple_code_review",
#     description="코드 리뷰를 수행하는 간단한 프롬프트 에이전트",
#     input_keys=["input"],
#     output_key="code_review",
#     prompt_template="다음 코드를 리뷰해줘:\n\n{code}",
#     save_path='test_agent.json'
# )

# res = run_single_qa(
#     input="def foo(): return 1/0",
#     agent_name="simple_code_review",
#     model="chatgpt",
#     model_type="gpt-3.5-turbo"
# )

# print(res["code_review"])

##### Json으로 저장한 다음에 Agent 다시 불러오고 Agent등록되어있는 것도 확인!!
# from qa_agent.engine.registry import list_agents
# load_prompt_aget('./test_agent.json')
# print(list_agents())