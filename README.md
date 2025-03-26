# Test Automation Multi Agent System Using LLM
이 프로젝트는 코드 변경을 자동으로 감지하고 이에 맞는 자동화된 테스트 케이스와 스크립트를 생성하는 QA Agent를 개발합니다. 지속적인 통합 및 지속적인 배포 (CICDCT) 환경에 대응하기 위해 설계된 이 도구는, 코드 변경을 실시간으로 분석하고, 해당 변경에 맞는 테스트를 자동으로 생성합니다.
## Overview
This project leverages advanced AI techniques to automate the generation of test scripts for software applications. Using language models like GPT, it analyzes test cases and automatically generates Python test scripts using popular testing frameworks like `pytest`, `Selenium`, and `Playwright`.

The goal of this project is to create an AI-driven tool that significantly reduces the effort and time required for software testing by automating the generation of test cases and corresponding Python code.

## Features
- **Test Case Analysis**: Automatically analyzes input test cases and identifies the necessary steps for testing.
- **Test Script Generation**: Uses AI to generate Python test scripts using various testing frameworks like `pytest`, `Selenium`, and `Playwright`.
- **Modular and Maintainable Code**: The generated test scripts follow best practices for readability and maintainability, with support for setup/teardown, fixtures, and assertions.
- **Flexible Framework Support**: Easily extendable to support different testing frameworks and libraries.

## How It Works
1. **Input Test Cases**: Provide detailed test cases describing software features and expected behavior.
2. **AI-Powered Test Code Generation**: The tool analyzes the input and generates Python test scripts with detailed comments describing the test objectives, steps, and expected results.
3. **Customization**: You can choose between multiple testing frameworks like `pytest`, `Selenium`, and `Playwright`.
4. **Output**: The generated test scripts are ready for execution, ensuring fast and accurate testing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/test-automation-agent.git
