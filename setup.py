from setuptools import setup, find_packages

setup(
    name="qa-agent-lib",
    version="0.1.0",
    description="LLM 기반 QA 자동화 프레임워크",
    author="JongyunShin",
    packages=find_packages(),  # 'qa_agent'를 포함시킴
    install_requires=[
        "openai",
        "langchain",
        "langgraph",
        "pyyaml"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "qa-agent = cli.main:main"
        ]
    },
)
