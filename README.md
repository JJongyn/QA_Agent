# requirements.txt
openai>=1.0.0
langgraph>=0.0.10
langchain>=0.1.0
pyyaml>=6.0

# README.md
# QA-Agent-Lib

A modular LLM-powered framework for automated code review, test generation, and QA workflows.

## ✅ Features

- 🤖 LangGraph-compatible QA agents (code review, test generation, etc.)
- ⚙️ YAML-based workflow configuration
- 🧠 Pluggable LLM backends (OpenAI, etc.)
- 🔀 Conditional branching support
- 💻 CLI for single-agent or full pipeline execution

## 📦 Installation

```bash
# (recommended) create a conda environment first
conda create -n qa_agent python=3.9 -y
conda activate qa_agent

# install with editable mode
pip install -e .
```

## 🚀 Quick Start

### 1. Write your code to be analyzed:

```python
# examples/test_code.py
def is_even(n):
    return n % 2 == 0
```

### 2. Define your workflow in YAML:

```yaml
# workflows/review_and_test.yaml
nodes:
  - name: review
    agent: code_review
  - name: testgen
    agent: test_case_generator
edges:
  - from: review
    to: testgen
```

### 3. Run it!

```bash
qa-agent run \
  --workflow workflows/review_and_test.yaml \
  --file examples/test_code.py \
  --llm chatgpt \
  --model gpt-3.5-turbo
```

### Example Output:
```
[code_review]
코드는 간단하며 명확합니다... 

[generated_test]
import unittest
...
```

## 🧩 Agent Types
- `code_review`: Analyze and comment on given code
- `test_case_generator`: Generate unit tests
- (you can add your own!)

## 📚 How to Add Your Own Agent

Create a new file in `agents/`, and inherit from `BaseAgent`:

```python
from agents.base import BaseAgent
from engine.registry import register_agent

class MyAgent(BaseAgent):
    name = "my_agent"
    input_keys = ["code"]
    output_keys = ["my_result"]

    def run(self, state: dict) -> dict:
        result = self.llm.generate("Do something with " + state["code"])
        state["my_result"] = result
        return state

register_agent("my_agent", MyAgent)
```

Then just add it to your YAML and you're done!
