from google.genai import types
import os

SCHEMA = types.FunctionDeclaration(
    name="save_text_file",
    description="주어진 텍스트 내용을 파일에 저장합니다. (이미지 등 바이너리 파일은 지원하지 않습니다. UTF-8 인코딩 사용)",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "filename": types.Schema(type="STRING", description="저장할 파일의 이름 (확장자 포함)"),
            "content": types.Schema(type="STRING", description="파일에 저장할 내용 (Python 코드 등 긴 문자열 가능)"),
        },
        required=["filename", "content"],
    ),
)

def main(filename: str, content: str) -> str:
    # 보안: 상위 디렉토리 접근 제한
    if ".." in filename or filename.startswith("/"):
        return "Error: 현재 디렉토리 및 하위 디렉토리에만 파일을 저장할 수 있습니다."
    
    try:
        # 파일 저장 (utf-8, 덮어쓰기 모드)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"파일 '{filename}'이(가) 성공적으로 저장되었습니다."
    except Exception as e:
        return f"Error saving file: {e}"

if __name__ == "__main__":
    print(SCHEMA.model_dump_json(indent=2))
