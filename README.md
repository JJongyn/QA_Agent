# 🧠 QA Agent Framework

A modular framework to automate code QA with LLM-powered agents  
(code review, bug detection, test generation, refactoring, and more).


## ✨ Features

- 🤖 Built-in QA agents for code analysis
- 🧱 Multi-step workflows with LangGraph
- 💬 Natural language to multi-agent automation
- 🧩 Pluggable custom agent creation (SDK)
- 📄 Unified JSON output format



## 🚀 Installation

```bash
pip install qa-agent-lib
```


## 🔧 CLI Usage

### 1. Run a full multi-step QA workflow
```bash
qa-agent run \
  --workflow workflows/review_and_test.yaml \
  --file e
```

### 2. Run a single agent
```bash
qa-agent run-agent \
  --agent code_review \
  --file examples/test_code.py
```
### 3. Run auto QA from natural language query
```bash
qa-agent auto \
  --query "Please review and test this code" \
  --file examples/test_code.py
```  


## 🧪 Built-in QA Agents
| Agent Name             | Description                                       | Output Key            |
|------------------------|---------------------------------------------------|------------------------|
| `code_review`          | Review code for bugs, structure, and readability  | `code_review`          |
| `bug_detection`        | Detect exceptions, edge cases, or logic bugs      | `bugs_found`           |
| `test_case_generator`  | Generate unit test cases                          | `generated_test`       |
| `refactor_suggester`   | Suggest performance and readability improvements  | `refactor_suggestion`  |
| `complexity_analyzer`  | Analyze cyclomatic complexity & structure         | `complexity_feedback`  |
| `docstring_generator`  | Generate docstrings for functions and classes     | `docstring`            |
| `qa_report_generator`  | Summarize all outputs into a final markdown report| `qa_report`            |

## 🧰 Create Your Own Agent

You can easily define your own QA agent using a prompt template:

```python
from qa_agent.sdk.prompt_agent import create_prompt_agent

create_prompt_agent(
    name="security_checker",
    description="Check for security risks",
    input_keys=["code"],
    output_key="security_risks",
    prompt_template="""
      You are a security expert.
      Analyze the following code for vulnerabilities, insecure patterns, and risks.

      Respond in JSON format:
      {
        "summary": "High-level overview of security findings",
        "risks": [
          "Line 10: Hardcoded credentials",
          "Line 24: Missing input validation"
        ]
      }

      Code:
{code}
"""
)
```

## 💾 Save and Load Custom Agents

You can save your custom agents to disk and load them later for reuse.

### Save to JSON
```python
create_prompt_agent(..., save_path="saved/security_checker.json")
```

### Load from JSON
```python
load_prompt_agent("saved/security_checker.json")
```