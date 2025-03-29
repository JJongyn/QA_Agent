import argparse
import json
import sys
import os

from pathlib import Path

from engine.registry import get_agent
from engine.workflow import WorkflowEngine
from llm.chatgpt import ChatGPTLLM

def load_llm(model: str, model_type: str):
    if model == "chatgpt":
        return ChatGPTLLM(model=model_type)
    else:
        raise NotImplementedError(f"LLM model {model} is not supported yet.")
    
def load_input(args) -> dict:
    if args.input:
        return json.loads(args.input)
    elif args.file:
        code = Path(args.file).read_text(encoding="utf-8")
        return {"code": code}
    elif not sys.stdin.isatty():
        # 표준입력 처리
        code = sys.stdin.read()
        return {"code": code}
    else:
        raise ValueError("입력이 제공되지 않았습니다. --input, --file, stdin 중 하나는 필요합니다.")

# langgrpah - workflow 실행을 위해
def run_workflow(args):
    state = load_input(args)
    llm = load_llm(model=args.llm, model_type=args.model)

    engine = WorkflowEngine()

    def review_judge(state):
        if "bug" in state.get("code_review", ""):
            return "needs_fix"
        return "clean"

    engine.register_condition("review_judge", review_judge)
    engine.load_from_yaml(args.workflow, llm=llm)
    result = engine.run(state)

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 결과 저장됨: {args.output}")
    else:
        print("📋 결과:")
        for k, v in result.items():
            print(f"\n[{k}]\n{v}")
            
def run_single_agent(args):
    state = load_input(args)
    llm = load_llm(backend=args.llm, model=args.model)

    AgentClass = get_agent(args.agent)
    agent = AgentClass(llm=llm)

    result = agent(state)

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 결과 저장됨: {args.output}")
    else:
        print("📋 결과:")
        for k, v in result.items():
            print(f"\n[{k}]\n{v}")
            
def main():
    parser = argparse.ArgumentParser(description="General QA Agent CLI")
    subparsers = parser.add_subparsers(dest="command")

    # run workflow
    run_parser = subparsers.add_parser("run", help="워크플로우 실행")
    run_parser.add_argument("--workflow", required=True, help="워크플로우 YAML 경로")
    input_group = run_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", help="JSON 문자열 입력")
    input_group.add_argument("--file", help="코드 파일 경로")
    run_parser.add_argument("--llm", default="chatgpt", help="LLM 백엔드 (기본: chatgpt)")
    run_parser.add_argument("--model", default="gpt-3.5-turbo", help="LLM 모델")
    run_parser.add_argument("--output", help="결과 저장 경로 (json)")

    # run single agent
    agent_parser = subparsers.add_parser("run-agent", help="단일 Agent 실행")
    agent_parser.add_argument("--agent", required=True, help="Agent 이름 (registry 등록된 이름)")
    agent_parser.add_argument("--llm", default="chatgpt", help="LLM 백엔드")
    agent_parser.add_argument("--model", default="gpt-3.5-turbo", help="LLM 모델")
    agent_parser.add_argument("--input", help="JSON 문자열 입력")
    agent_parser.add_argument("--file", help="코드 파일 경로")
    agent_parser.add_argument("--output", help="결과 저장 경로 (json)")

    args = parser.parse_args()

    if args.command == "run":
        run_workflow(args)
    elif args.command == "run-agent":
        run_single_agent(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
