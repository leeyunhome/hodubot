from google.genai import types

SCHEMA = types.FunctionDeclaration(
    name="add_two_numbers",
    description="두 숫자를 더합니다.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "a": types.Schema(type="NUMBER", description="첫 번째 숫자"),
            "b": types.Schema(type="NUMBER", description="두 번째 숫자"),
        },
        required=["a", "b"],
    ),
)

def execute(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    # TODO: argument 없이 이 파일을 실행시켰을 경우 schema를 반환하도록 구조 변경 (이 파일만 변경하고 main.py 는 그대로 두고 나중에 처리)
    print(SCHEMA.model_dump_json(indent=2))