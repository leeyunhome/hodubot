# Tools 폴더 가이드

## 필수 구조

```python
from google.genai import types

SCHEMA = types.FunctionDeclaration(
    name="example_tool",
    description="도구 설명 (AI가 언제 사용할지 판단하는 핵심)",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "param1": types.Schema(type="STRING", description="파라미터 설명"),
        },
        required=["param1"],
    ),
)

def main(param1: str) -> str:
    # 로직 구현
    return "결과 문자열"
```

## 파라미터 타입

| Schema Type | Python Type |
|-------------|-------------|
| `STRING` | `str` |
| `INTEGER` | `int` |
| `NUMBER` | `float` |
| `BOOLEAN` | `bool` |

## 보안 주의사항

파일 시스템 접근 시 상위 폴더 탈출 방지 필수:

```python
import os

def main(path: str) -> str:
    base_dir = os.getcwd()
    resolved = os.path.realpath(path)
    
    if not resolved.startswith(base_dir):
        return "오류: 허용되지 않은 경로"
    
    # 안전한 경우에만 진행
    ...
```
