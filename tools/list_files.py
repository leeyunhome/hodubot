from google.genai import types
import os

SCHEMA = types.FunctionDeclaration(
    name="list_files",
    description="주어진 디렉토리의 파일 목록을 나열합니다.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "path": types.Schema(type="STRING", description="파일 목록을 확인할 디렉토리 경로 (기본값: 현재 디렉토리)"),
        },
        required=[],
    ),
)

def main(path: str = ".") -> str:
    try:
        base_dir = os.getcwd()
        target_path = os.path.abspath(path)
        
        # Check if target_path starts with base_dir
        if not target_path.startswith(base_dir):
             return "Error: 접근이 거부되었습니다. 현재 디렉토리와 그 하위 디렉토리만 조회할 수 있습니다."
             
        files = os.listdir(path)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(SCHEMA.model_dump_json(indent=2))
