import json
from pathlib import Path
from typing import Optional

from qa_agent.core.registry import register_agent
from qa_agent.agents.base import BaseAgent

'''
Agent SDK
'''

def create_prompt_agent(name: str, description: str, input_keys: list, output_key: str, prompt_template: str, save_path: Optional[str] = None):
    def build_prompt(self, code: str) -> str:
        return prompt_template.format(code=code)

    def run(self, state: dict) -> dict:
        code = state.get("input", "")
        if not code:
            raise ValueError("입력 state에 'input' 키가 없습니다.")

        prompt = self.build_prompt(code)
        response = self.llm.generate(prompt) if self.llm else "[응답 없음]: LLM을 설정해주세요."
        state[output_key] = response
        return state

    def run_with_input(self, code: str) -> str:
        return self.run({"input": code})[output_key]

    AgentClass = type(
        f"{name.title().replace('_', '')}Agent",
        (BaseAgent,),
        {
            "name": name,
            "description": description,
            "input_keys": ["input"],  # LangGraph와 일관성 있게
            "output_keys": [output_key],
            "build_prompt": build_prompt,
            "run": run,
            "run_with_input": run_with_input,
        }
    )

    register_agent(name, AgentClass)
    
    if save_path:
        save_agent(
            path=save_path,
            name=name,
            description=description,
            input_keys=input_keys,
            output_key=output_key,
            prompt_template=prompt_template
        )
        print("Saved your Agent!")

def save_agent(path: str, **kwargs):
    config = {
        "type": "agent",
        **kwargs
    }
    Path(path).write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    
def load_agent(path: str):
    config = json.loads(Path(path).read_text(encoding="utf-8"))

    if config.get("type") != "agent":
        raise ValueError("지원하지 않는 Agent 타입입니다.")

    create_prompt_agent(
        name=config["name"],
        description=config["description"],
        input_keys=config["input_keys"],
        output_key=config["output_key"],
        prompt_template=config["prompt_template"]
    )
    