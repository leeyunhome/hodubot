from google.genai import types
from datetime import datetime

SCHEMA = types.FunctionDeclaration(
    name="get_current_time",
    description="현재 시간과 날짜를 가져옵니다. 시간을 물어보면 이 도구를 사용하세요.",
    parameters=types.Schema(
        type="OBJECT",
        properties={},
        required=[],
    ),
)

def main() -> str:
    """현재 시스템 시간을 반환합니다."""
    now = datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")

if __name__ == "__main__":
    print(main())
