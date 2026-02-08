from google.genai import types
import os

SCHEMA = types.FunctionDeclaration(
    name="read_text_file",
    description="주어진 텍스트 파일의 내용을 읽어옵니다. (UTF-8 인코딩 사용). 파일 경로는 상대 경로를 정확히 입력해야 합니다 (예: tools/file.py)",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "filename": types.Schema(type="STRING", description="읽을 파일의 이름 (확장자 포함)"),
        },
        required=["filename"],
    ),
)

def main(filename: str) -> str:
    # 보안: 상위 디렉토리 접근 제한
    if ".." in filename or filename.startswith("/"):
        return "Error: 현재 디렉토리 및 하위 디렉토리의 파일만 읽을 수 있습니다."
    
    if not os.path.exists(filename):
        return f"Error: 파일 '{filename}'을(를) 찾을 수 없습니다."

    try:
        # 파일 읽기 (utf-8)
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    import sys
    # 인자가 있으면 해당 파일 읽기 (테스트 용도)
    if len(sys.argv) > 1:
        print(main(sys.argv[1]))
    else:
        print(SCHEMA.model_dump_json(indent=2))
