from setuptools import setup, find_packages

setup(
    name="qa-agent-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "langgraph",
        "langchain",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "qa-agent = cli.main:main"
        ]
    },
    author="JongyunShin",
    description="LLM-based QA Agent Framework",
    python_requires=">=3.8",
)
