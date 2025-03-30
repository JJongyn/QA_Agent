# engine/auto_selector.py

from typing import List, Dict, Optional
from .workflow import WorkflowEngine
from .registry import get_agent, list_agents
from qa_agent.llm.chatgpt import ChatGPTLLM


def get_all_agent_descriptions() -> Dict[str, str]:
    """
    각 Agent 클래스의 description 속성을 읽어와서 반환
    """
    descriptions = {}
    for name, AgentClass in list_agents().items():
        desc = getattr(AgentClass, "description", "No description provided.")
        descriptions[name] = desc
    return descriptions


def llm_select_agents(user_request: str, llm: ChatGPTLLM) -> List[str]:
    """
    LLM에게 사용자 요청을 기반으로 적절한 Agent 이름을 추론하게 함
    """
    agent_descriptions = get_all_agent_descriptions()
    agent_list_text = "\n".join([
        f"- {name}: {desc}" for name, desc in agent_descriptions.items()
    ])

    prompt = f"""
    아래는 사용 가능한 QA Agent 목록입니다:
    {agent_list_text}

    사용자의 요청:
    "{user_request}"

    위 요청에 가장 적절한 에이전트 이름만 골라서 파이썬 리스트 형태로 응답해주세요. (예: ['code_review', 'bug_detection'])
    """

    response = llm.generate(prompt)
    try:
        parsed = eval(response.strip())
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    return []


def llm_suggest_edges(agent_names: List[str], llm: ChatGPTLLM) -> List[tuple]:
    """
    LLM에게 노드 간 연결 순서를 제안받아 edges를 생성함
    """
    agent_descriptions = get_all_agent_descriptions()
    agent_list_text = "\n".join([
        f"- {name}: {desc}" for name, desc in agent_descriptions.items() if name in agent_names
    ])

    prompt = f"""
    다음은 선택된 QA Agent 목록입니다:
    {agent_list_text}

    각 agent의 실행 순서를 고려하여, 어떤 agent가 어떤 agent 다음에 실행되어야 하는지 edge 목록을 파이썬 튜플 리스트로 작성해주세요. (예: [('code_review', 'test_case_generator'), ('test_case_generator', 'qa_report_generator')])
    """

    response = llm.generate(prompt)

    try:
        parsed = eval(response.strip())
        if isinstance(parsed, list) and all(isinstance(pair, tuple) and len(pair) == 2 for pair in parsed):
            return parsed
    except Exception:
        pass

    return []


def auto_build_workflow(user_request: str, llm: ChatGPTLLM, include_report: bool = False) -> WorkflowEngine:
    """
    사용자의 요청에 따라 자동으로 적절한 에이전트들을 선택하고 워크플로우 구성
    """
    selected_agents = llm_select_agents(user_request, llm)
    
    engine = WorkflowEngine()
    name_map = {}
    
    print(selected_agents)
    # 기본 에이전트 등록
    for agent_name in selected_agents:
        node_name = agent_name.replace("_", "")
        name_map[agent_name] = node_name
        engine.add_agent(name=node_name, agent_name=agent_name, llm=llm)

    # edge 연결
    edge_list = llm_suggest_edges(selected_agents, llm)
    for src, dst in edge_list:
        if src in name_map and dst in name_map:
            engine.graph.add_edge(name_map[src], name_map[dst])

    if include_report:
        report_name = "qa_report_generator"
        report_node = report_name.replace("_", "")
        name_map[report_name] = report_node
        engine.add_agent(name=report_node, agent_name=report_name, llm=llm)

        if edge_list:
            last_dst = edge_list[-1][1]
            engine.graph.add_edge(name_map[last_dst], report_node)
        else:
            if selected_agents:
                first_node = selected_agents[0]
                engine.graph.add_edge(name_map[first_node], report_node)

    
    return engine



def run_general_qa(query: str, user_input: Optional[Dict[str, str]], llm: ChatGPTLLM, include_report: bool = False) -> dict:
    """
    사용자 질의(query)와 입력(user_input: code, requirements 등)을 받아
    적절한 Agent workflow를 구성하고 실행
    """
    engine = auto_build_workflow(query, llm, include_report)
    state = user_input if user_input else {}

    missing_inputs = {}
    for node in engine.graph.nodes:
        agent = engine.agents[node]
        missing = [k for k in agent.input_keys if k not in state]
        if missing:
            missing_inputs[node] = missing

    if missing_inputs:
        warning = "\n".join([
            f"⚠️ '{node}' Agent에 필요한 입력 누락: {', '.join(missing)}"
            for node, missing in missing_inputs.items()
        ])
        print("[입력 누락 경고]\n" + warning + "\n")
    return engine.run(state)
