from google.genai import types

SCHEMA = types.FunctionDeclaration(
    name="subtract_two_numbers",
    description="첫 번째 숫자에서 두 번째 숫자를 뺍니다.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "a": types.Schema(type="NUMBER", description="첫 번째 숫자"),
            "b": types.Schema(type="NUMBER", description="두 번째 숫자"),
        },
        required=["a", "b"],
    ),
)

def main(a: int, b: int) -> int:
    return a - b

if __name__ == "__main__":
    print(SCHEMA.model_dump_json(indent=2))
