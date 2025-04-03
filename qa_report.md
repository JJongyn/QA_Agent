## Query
이 코드에 대해 리뷰하고 text case 생성해줘

## Code Review
### 🔍 리뷰 대상 코드:

```python
    def find_average(lst):
    sum = 0
    for num in lst:
    sum += num
    return sum / len(lst)
```

### 📝 리뷰:
1. **코드 스타일 및 포매팅:**
   - 함수명과 변수명은 snake_case 대신 camelCase를 사용하고 있습니다. Python의 일반적인 규칙은 snake_case를 따르므로 이를 수정하는 것이 좋습니다.
   - 들여쓰기가 일관되지 않고, 함수 정의와 for 루프 내부의 들여쓰기가 맞지 않습니다. 코드를 더 가독성 있게 작성하기 위해 들여쓰기를 조정해야 합니다.

2. **가독성과 유지보수성:**
   - 코드가 간단하고 직관적이지만, 들여쓰기와 스타일의 일관성이 부족하여 가독성이 떨어집니다. 
   - 변수명이 좀 더 설명적으로 작성되면 이해하기 쉬울 것입니다.

3. **버그 가능성 또는 논리적 문제:**
   - 코드 자체에는 큰 버그는 없어 보입니다. 그러나 lst가 비어있는 경우에는 ZeroDivisionError가 발생할 수 있습니다. 이러한 예외 상황을 처리해주는 로직이 필요합니다.

4. **개선을 위한 제안:**
   - 함수명과 변수명을 snake_case로 변경하고, 일관된 들여쓰기를 유지하도록 수정해야 합니다.
   - 빈 리스트 예외를 처리하기 위한 로직을 추가해야 합니다.
   - 변수명을 좀 더 의미 있게 작성하여 코드의 이해를 돕는 것이 좋습니다.
```

## Generated Test
{
    "summary": "주어진 Python 함수의 유효성을 검증하기 위한 테스트 케이스들을 작성했습니다. 주어진 함수는 입력된 숫자에 2를 곱한 값을 반환하는 간단한 기능을 수행합니다.",
    "test_framework": "pytest",
    "test_cases": [
        {
            "name": "test_valid_input",
            "description": "유효한 입력값에 대한 테스트",
            "code": "def test_valid_input():\n    assert my_function(2) == 4"
        },
        {
            "name": "test_negative_input",
            "description": "음수 입력값에 대한 테스트",
            "code": "def test_negative_input():\n    assert my_function(-3) == -6"
        },
        {
            "name": "test_zero_input",
            "description": "0을 입력했을 때의 테스트",
            "code": "def test_zero_input():\n    assert my_function(0) == 0"
        },
        {
            "name": "test_large_input",
            "description": "큰 숫자를 입력했을 때의 테스트",
            "code": "def test_large_input():\n    assert my_function(1000000) == 2000000"
        }
    ]
}
