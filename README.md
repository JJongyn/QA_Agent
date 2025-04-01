# QA Agent Framework

LLM 기반 에이전트를 활용하여 Software QA를 지원하는 모듈형 프레임워크입니다.  
(코드 리뷰, 버그 탐지, 테스트 생성, 리팩토링 등 다양한 QA 작업 지원)

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
    query="Review this function and write test cases.",
    input="def add(a, b): return a + b",
    model="chatgpt",
    model_type="gpt-3.5-turbo"
)
print(result["qa_report"])
```

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

