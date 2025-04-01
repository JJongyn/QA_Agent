import argparse
import json
import sys
import os

from pathlib import Path

from core.auto_selector import run_general_qa
from core.registry import get_agent
from core.workflow import WorkflowEngine
from models.chatgpt import ChatGPTLLM
from utils.util import *

# langgrpah - workflow 실행을 위해
def run_workflow(args):
    state = load_input(args)
    llm = load_llm(model=args.llm, model_type=args.model)

    engine = WorkflowEngine()

    # def review_judge(state):
    #     if "bug" in state.get("code_review", ""):
    #         return "needs_fix"
    #     return "clean"

    # engine.register_condition("review_judge", review_judge)
    
    engine.load_from_yaml(args.workflow, llm=llm)
    result = engine.run(state)
    print_result(args, result)
            
def run_single_agent(args):
    state = load_input(args)
    llm = load_llm(model=args.llm, model_type=args.model)

    AgentClass = get_agent(args.agent)
    agent = AgentClass(llm=llm)

    result = agent(state)
    print_result(args, result)

def run_auto(args):
    state = load_input(args)
    llm = load_llm(model=args.llm, model_type=args.model)
    result = run_general_qa(query=args.query, user_input=state, llm=llm, include_report=args.summary_only)

    print_result(args, result)


def main():
    parser = argparse.ArgumentParser(description="General QA Agent CLI")
    subparsers = parser.add_subparsers(dest="command")

    # run workflow
    run_parser = subparsers.add_parser("run", help="워크플로우 실행")
    run_parser.add_argument("--workflow", required=True, help="워크플로우 YAML 경로")
    run_parser.add_argument("--summary-only", action="store_true", help="qa_report 만 출력 (요약 모드)")
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
    agent_parser.add_argument("--summary-only", action="store_true", help="qa_report 만 출력 (요약 모드)")
    
    # auto mode
    auto_parser = subparsers.add_parser("auto", help="자연어 기반 자동 QA 실행")
    auto_parser.add_argument("--query", required=True, help="자연어 요청")
    auto_parser.add_argument("--input", help="JSON 문자열 또는 파일 경로")
    auto_parser.add_argument("--file", help="코드 파일 경로")
    auto_parser.add_argument("--llm", default="chatgpt", help="LLM 백엔드")
    auto_parser.add_argument("--model", default="gpt-3.5-turbo", help="LLM 모델")
    auto_parser.add_argument("--output", help="결과 저장 경로 (json)")
    auto_parser.add_argument("--summary-only", action="store_true", help="qa_report 만 출력 (요약 모드)")

    
    args = parser.parse_args()

    command_map = {
        "run": run_workflow,
        "run-agent": run_single_agent,
        "auto": run_auto
    }

    if args.command in command_map:
        command_map[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
