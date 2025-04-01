import os
import sys
import json

from pathlib import Path

from .models.chatgpt import ChatGPTLLM

'''
입출력 관련 Utils
'''
def load_llm(model: str, model_type: str):
    if model == "chatgpt":
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다.")
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
        input = sys.stdin.read()
        return {"input": input}
    else:
        raise ValueError("입력이 제공되지 않았습니다. --input, --file, stdin 중 하나는 필요합니다.")

def print_result(args, result):
    if getattr(args, "output", None):
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"결과 저장됨: {args.output}")

    if getattr(args, "summary_only", False):
        print("\n최종 요약 리포트 (qa_report):\n")
        print(result.get("qa_report", "[요약 리포트 없음]"))
    elif not getattr(args, "output", None):
        print("\n전체 결과:")
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