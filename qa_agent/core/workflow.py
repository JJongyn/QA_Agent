import yaml
from typing import Dict, Any

from langgraph.graph import StateGraph
from .registry import find_agent

class WorkflowEngine:
    def __init__(self):
        self.graph = StateGraph(state_schema=Dict[str, Any])
        self.entry = None
        self.last = None
        self.node_sequence = []  # 순서 추적용
        self.conditions = {}
        self.agents = {}
        
    def add_agent(self, name: str, agent_name: str, llm=None, tags=None):
        AgentClass = find_agent(agent_name)
        agent = AgentClass(llm=llm)

        # tag 저장용 attribute 부여
        agent._tags = tags or []
        self.graph.add_node(name, agent)
        self.agents[name] = agent

        if self.entry is None:
            self.entry = name
        else:
            self.graph.add_edge(self.last, name)

        self.last = name
        self.node_sequence.append((name, agent_name, tags))

    def add_branch(self, from_node: str, condition_fn, branches: dict):
        """
        from_node: 분기 시작 노드
        condition_fn: 상태 기반 조건 함수 (state -> key)
        branches: {key: 노드이름}
        """
        self.graph.add_conditional_edges(
            from_node,
            condition_fn,
            branches
        )
    
    def register_condition(self, name:str, fn):
        self.conditions[name] = fn

    def compile(self):
        self.graph.set_entry_point(self.entry)
        return self.graph.compile()

    def run(self, input_state: dict):
        runner = self.compile()
        return runner.invoke(input_state)

    def describe(self):
        print("\n🧩 [Workflow Description]")
        print("Entry Point:", self.entry)
        for name, agent_name, tags in self.node_sequence:
            tag_str = ", ".join(tags or [])
            print(f"- Node: {name} | Agent: {agent_name} | Tags: {tag_str}")

    def load_from_yaml(self, path: str, llm=None):
        """
        YAML 파일로부터 workflow 구성 자동화
        구조 예:
        nodes:
          - name: review
            agent: code_review
            tags: [review]
          - name: test
            agent: test_case_generator
            tags: [test]
        edges:
          - from: review
            to: test
        """
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        # 노드 등록
        for node in config.get("nodes", []):
            self.add_agent(
                name=node["name"],
                agent_name=node["agent"],
                llm=llm,
                tags=node.get("tags", [])
            )

        # 연결 구성
        for edge in config.get("edges", []):
            self.graph.add_edge(edge["from"], edge["to"])

        for cond in config.get("conditions", []):
            node = cond["node"]
            cond_name = cond["using"]
            branches = cond["branches"]
            
            if cond_name not in self.conditions:
                raise ValueError(f"조건 함수 '{cond_name}'가 등록되어 있지 않습니다.")
            
            self.add_branch(
                from_node=node,
                condition_fn=self.conditions[cond_name],
                branches=branches
            )
            
        self.describe()