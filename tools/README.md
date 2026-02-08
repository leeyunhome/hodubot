# 🛠️ 호두봇 도구(Tool) 개발 가이드

## 개요
`tools/` 폴더에 Python 파일(`.py`)을 추가하면, 호두봇이 자동으로 해당 도구를 로드하여 사용할 수 있습니다.

---

## 필수 구조

모든 도구 파일은 **두 가지 필수 요소**를 포함해야 합니다:

### 1. `SCHEMA` (도구 정의)
```python
from google.genai import types

SCHEMA = types.FunctionDeclaration(
    name="도구_이름",  # 영문 소문자 + 언더스코어 권장
    description="이 도구가 무엇을 하는지 한글로 설명",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "param1": types.Schema(type="STRING", description="파라미터 설명"),
            "param2": types.Schema(type="INTEGER", description="숫자 파라미터"),
        },
        required=["param1"],  # 필수 파라미터 목록
    ),
)
```

### 2. `main()` 함수 (실행 로직)
```python
def main(param1: str, param2: int = 0) -> str:
    """도구의 실제 동작을 구현합니다."""
    # 로직 구현
    result = f"처리 결과: {param1}, {param2}"
    return result  # 반드시 문자열 반환
```

---

## 지원하는 파라미터 타입

| Schema Type | Python Type | 설명 |
|-------------|-------------|------|
| `STRING` | `str` | 문자열 |
| `INTEGER` | `int` | 정수 |
| `NUMBER` | `float` | 실수 |
| `BOOLEAN` | `bool` | 참/거짓 |
| `ARRAY` | `list` | 배열 |
| `OBJECT` | `dict` | 객체 |

---

## 보안 주의사항 ⚠️

### 1. 경로 검증 (필수)
파일 시스템을 다루는 도구는 **상위 디렉토리 접근을 차단**해야 합니다:
```python
import os

def main(path: str) -> str:
    base_dir = os.getcwd()
    target = os.path.abspath(path)
    
    # 보안 검사: 프로젝트 폴더 밖으로 나가는 것 방지
    if not target.startswith(base_dir):
        return "오류: 허용되지 않은 경로입니다."
    
    # 안전한 경우에만 진행
    ...
```

### 2. 위험한 명령어 실행 금지
- `os.system()`, `subprocess.run()` 사용 시 사용자 입력을 직접 삽입하지 마세요.
- 필요한 경우 화이트리스트 방식으로 허용된 명령만 실행하세요.

---

## 좋은 도구 설계 원칙

1. **명확한 설명**: `description`은 AI가 도구를 언제 사용할지 판단하는 핵심입니다.
2. **단일 책임**: 하나의 도구는 하나의 기능만 수행하세요.
3. **에러 처리**: 예외 상황에서도 친절한 에러 메시지를 반환하세요.
4. **반환값은 문자열**: `main()` 함수는 항상 `str`을 반환해야 합니다.

---

## 예제: 간단한 계산기 도구

```python
from google.genai import types

SCHEMA = types.FunctionDeclaration(
    name="calculator",
    description="두 숫자를 더하거나 빼거나 곱하거나 나눕니다.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "a": types.Schema(type="NUMBER", description="첫 번째 숫자"),
            "b": types.Schema(type="NUMBER", description="두 번째 숫자"),
            "operation": types.Schema(
                type="STRING", 
                description="연산자 (add, sub, mul, div)"
            ),
        },
        required=["a", "b", "operation"],
    ),
)

def main(a: float, b: float, operation: str) -> str:
    ops = {
        "add": a + b,
        "sub": a - b,
        "mul": a * b,
        "div": a / b if b != 0 else "Error: Division by zero",
    }
    result = ops.get(operation, "Error: Unknown operation")
    return str(result)
```

---

## 테스트 방법

도구 파일을 직접 실행하면 스키마를 확인할 수 있습니다:
```bash
python tools/your_tool.py
```

`main.py`를 재시작하면 새 도구가 자동으로 로드됩니다.

---

## 기존 도구 목록

| 파일명 | 기능 |
|--------|------|
| `list_files.py` | 디렉토리 파일 목록 조회 |
| `save_text_file.py` | 텍스트 파일 저장 |
| `read_text_file.py` | 텍스트 파일 읽기 |
| `play_audio.py` | 오디오 파일 재생 및 분석 |
