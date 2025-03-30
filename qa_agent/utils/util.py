import argparse
import json
import sys
import os
from pathlib import Path
from typing import Optional
from qa_agent.llm.chatgpt import ChatGPTLLM
from qa_agent.agents.base import BaseAgent
from qa_agent.core.registry import register_agent


#### 나중에 개발자 sdk로 뺴기!!
def create_prompt_agent(name: str, description: str, input_keys: list, output_key: str, prompt_template: str, save_path: Optional[str] = None):
    
    def build_prompt(self, code: str) -> str:
        # input이 string인 경우를 상정
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
        save_prompt_agent(
            path=save_path,
            name=name,
            description=description,
            input_keys=input_keys,
            output_key=output_key,
            prompt_template=prompt_template
        )
        print("Saved your Agent!")

def save_prompt_agent(path: str, **kwargs):
    config = {
        "type": "agent",
        **kwargs
    }
    Path(path).write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    
def load_prompt_aget(path: str):
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
    

################################################

def load_llm(model: str, model_type: str):
    if model == "chatgpt":
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("❌ OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")
        return ChatGPTLLM(model=model_type)
    else:
        raise NotImplementedError(f"LLM model {model} is not supported yet.")
    
def load_input(args) -> dict:
    if args.input:
        return json.loads(args.input)
    elif args.file:
        input = Path(args.file).read_text(encoding="utf-8")
        return {"input": input}
    elif not sys.stdin.isatty():
        # 표준입력 처리
        input = sys.stdin.read()
        return {"input": input}
    else:
        raise ValueError("입력이 제공되지 않았습니다. --input, --file, stdin 중 하나는 필요합니다.")

def print_result(args, result):
    if getattr(args, "output", None):
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 결과 저장됨: {args.output}")

    if getattr(args, "summary_only", False):
        print("\n📋 최종 요약 리포트 (qa_report):\n")
        print(result.get("qa_report", "[요약 리포트 없음]"))
    elif not getattr(args, "output", None):
        print("\n📋 전체 결과:")
        for k, v in result.items():
            print(f"\n[{k}]\n{v}")
            



def resolve_input(input_val) -> dict:
    if isinstance(input_val, dict):
        return input_val
    elif isinstance(input_val, str):
        path = Path(input_val)
        if path.exists():
            content = path.read_text(encoding="utf-8")
            try:
                return json.loads(content)  # json이면 dict로
            except json.JSONDecodeError:
                return {"input": content}    # 아니면 그냥 코드 문자열
        else:
            return {"input": input_val}      # 그냥 문자열 코드로 간주
    else:
        raise ValueError("input은 str 또는 dict 타입이어야 합니다.")


# def save_result(result, output_path, output_name='result.json'):
#     Path(output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
#     print(f"✅ 결과 저장됨: {output_path}")