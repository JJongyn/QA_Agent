# QA Agent Framework

![img](./image.png)

이 도구는 AI agent를 활용하고 싶은 QA 엔지니어들을 위한 가이드입니다. 우리는 코드 리뷰, 버그 탐지, 테스크 케이스 생성 등 반복적은 QA 작업을 LLM 기반의 Multi-agent를 통해 자동화하는데 사용할 수 있으며 복잡한 설정을 필요로 하지 않습니다.

[View in ENG](./docs/README.md)

## ✨ Features

- 다양한 QA 작업을 위한 기본 내장 에이전트 제공
- LangGraph 기반의 다단계 워크플로우 실행
- 자연어 요청만으로 적절한 멀티 에이전트를 자동 구성
- 사용자가 직접 정의할 수 있는 커스텀 에이전트 생성 기능 


## 🚀 Installation

```bash
pip install qa-agent-lib
```

## 🔧 Available SDK Functions
qa_agent 모듈에서 모든 기능을 쉽게 불러올 수 있습니다:

```python
from qa_agent import (
    run_auto_qa,
    run_workflow_qa,
    run_single_qa,
    create_prompt_agent,
    save_agent,
    load_agent,
    register_agent,
    get_agent,
)
``` 

## Quick Examples

### ✅ 1. Run a Auto Multi-Agent ⭐️

> 자연어 요청을 기반으로 **자동으로** 적절한 QA 에이전트를 선택하고 실행합니다.

```python
from qa_agent import run_auto_qa

result = run_auto_qa(
    query="이 코드에 대해 리뷰하고 text case 생성해줘",
    input="def add(a, b): return a + b",
    model="chatgpt",
    model_type="gpt-3.5-turbo"
)
print(result["qa_report"])
```

#### 실행 결과

1. 자동 노드 선택 결과
    * Node: codereview | Agent: code_review | Tags: 
    * Node: testcasegenerator | Agent: test_case_generator | Tags: 
    * Node: qareportgenerator | Agent: qa_report_generator | Tags: 

2. 연결된 엣지 결과
    * codereview ➜ testcasegenerator
    * testcasegenerator ➜ qareportgenerator

3. 최종 보고서 결과 (qa_report.md)
    ## Query
      이 코드에 대해 리뷰하고 text case 생성해줘

      ## Code Review
      ### 🔍 리뷰 대상 코드:

      ```python
      def find_average(lst):
      sum = 0
      for num in lst:
      sum += num
      return sum / len(lst)
      ```

      ### 📝 리뷰:
      1. **코드 스타일 및 포매팅:**
        - 함수명과 변수명은 snake_case 대신 camelCase를 사용하고 있습니다. Python의 일반적인 규칙은 snake_case를 따르므로 이를 수정하는 것이 좋습니다.
        - 들여쓰기가 일관되지 않고, 함수 정의와 for 루프 내부의 들여쓰기가 맞지 않습니다. 코드를 더 가독성 있게 작성하기 위해 들여쓰기를 조정해야 합니다.

      2. **가독성과 유지보수성:**
        - 코드가 간단하고 직관적이지만, 들여쓰기와 스타일의 일관성이 부족하여 가독성이 떨어집니다. 
        - 변수명이 좀 더 설명적으로 작성되면 이해하기 쉬울 것입니다.

      3. **버그 가능성 또는 논리적 문제:**
        - 코드 자체에는 큰 버그는 없어 보입니다. 그러나 lst가 비어있는 경우에는 ZeroDivisionError가 발생할 수 있습니다. 이러한 예외 상황을 처리해주는 로직이 필요합니다.

      4. **개선을 위한 제안:**
        - 함수명과 변수명을 snake_case로 변경하고, 일관된 들여쓰기를 유지하도록 수정해야 합니다.
        - 빈 리스트 예외를 처리하기 위한 로직을 추가해야 합니다.
        - 변수명을 좀 더 의미 있게 작성하여 코드의 이해를 돕는 것이 좋습니다.
      ```

      ## Generated Test
      {
          "summary": "주어진 Python 함수의 유효성을 검증하기 위한 테스트 케이스들을 작성했습니다. 주어진 함수는 입력된 숫자에 2를 곱한 값을 반환하는 간단한 기능을 수행합니다.",
          "test_framework": "pytest",
          "test_cases": [
              {
                  "name": "test_valid_input",
                  "description": "유효한 입력값에 대한 테스트",
                  "code": "def test_valid_input():\n    assert my_function(2) == 4"
              },
              {
                  "name": "test_negative_input",
                  "description": "음수 입력값에 대한 테스트",
                  "code": "def test_negative_input():\n    assert my_function(-3) == -6"
              },
              {
                  "name": "test_zero_input",
                  "description": "0을 입력했을 때의 테스트",
                  "code": "def test_zero_input():\n    assert my_function(0) == 0"
              },
              {
                  "name": "test_large_input",
                  "description": "큰 숫자를 입력했을 때의 테스트",
                  "code": "def test_large_input():\n    assert my_function(1000000) == 2000000"
              }
          ]
      }

### ✅ 2. Run a single QA agent
> 특정 에이전트 하나만 선택해서 직접 실행합니다 (예: 코드 리뷰만 수행).

```python
from qa_agent import run_single_qa

result = run_single_qa(
    input="def subtract(a, b): return a - b",
    agent_name="code_review",
    model="chatgpt",
    model_type="gpt-3.5-turbo"
)
print(result["code_review"])
```

### ✅ 3. Run a predefined workflow for Multi-Agent ⭐️

> LangGraph 기반 멀티스텝 QA 파이프라인을 .yaml 파일로 정의하고 실행할 수 있습니다.
각 QA Agent는 노드(Node)로, 실행 순서는 엣지(Edge)로 구성되며, 복잡한 Multi-agent 시나리오도 쉽게 구현 가능합니다.

예를 들어 아래와 같은 .yaml 구성:

```yaml
nodes:
  - name: code_review
    agent: code_review
  - name: test_gen
    agent: test_case_generator
  - name: reporter
    agent: qa_report_generator

edges:
  - source: code_review
    target: test_gen
  - source: test_gen
    target: reporter
```
이렇게 정의된 흐름을 아래와 같이 실행할 수 있습니다:

```python
from qa_agent import run_workflow_qa

result = run_workflow_qa(
    input="def divide(a, b): return a / b",
    model="chatgpt",
    model_type="gpt-3.5-turbo",
    yaml_path="workflows/review_and_test.yaml"
)
print(result)
```

### ✅ 4. Create your own QA agent

> 프롬프트 템플릿만으로 사용자 정의 에이전트를 간편하게 생성합니다.

```python
from qa_agent import create_prompt_agent

create_prompt_agent(
    name="security_checker",
    description="Check code for security issues.",
    input_keys=["code"],
    output_key="security_risks",
    prompt_template="""
You are a security expert.
Analyze the following code and list any vulnerabilities in JSON format.

Code:
{code}
"""
)
```

### ✅ 5. Agent Utils

> 사용자가 직접 만든 에이전트를 로컬에 저장하거나 다시 불러올 수 있습니다.
또한, 에이전트를 등록하거나 등록된 에이전트 목록을 조회하는 기능도 함께 제공합니다.

```python
from qa_agent import save_agent, load_agent

# Save to disk
save_agent("security_checker", path="saved/security_checker.json")

# Load it later
load_agent(path="saved/security_checker.json")

# Resgister Agent
register_agent("Code_reviwer", CodeReviewer())

# Get stored Agent
get_agent() # ['Code_reviwer', 'bug_detect', 'test_case_gent' ...]
```



## 🧪 Built-in QA Agents

> 이 패키지에는 사전 정의된 QA 전문가 에이전트들이 포함되어 있습니다.
사용자는 언제든지 get_agent를 통해 등록된 모든 에이전트 목록을 조회할 수 있습니다.

| Agent Name             | Description                                       | Output Key            |
|------------------------|---------------------------------------------------|------------------------|
| `code_review`          | Review code for bugs, structure, and readability  | `code_review`          |
| `bug_detection`        | Detect exceptions, edge cases, or logic bugs      | `bugs_found`           |
| `test_case_generator`  | Generate unit test cases                          | `generated_test`       |
| `refactor_suggester`   | Suggest performance and readability improvements  | `refactor_suggestion`  |
| `complexity_analyzer`  | Analyze cyclomatic complexity & structure         | `complexity_feedback`  |
| `docstring_generator`  | Generate docstrings for functions and classes     | `docstring`            |
| `qa_report_generator`  | Summarize all outputs into a final markdown report| `qa_report`            |

