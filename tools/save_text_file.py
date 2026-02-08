from google.genai import types
import os

SCHEMA = types.FunctionDeclaration(
    name="save_text_file",
    description="주어진 텍스트 내용을 파일에 저장합니다. .py, .txt 등 확장자에 관계없이 모든 텍스트 내용을 저장할 수 있습니다. (내용 유효성 검사 없음)",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "filename": types.Schema(type="STRING", description="저장할 파일의 이름 (확장자 포함)"),
            "content": types.Schema(type="STRING", description="파일에 저장할 내용 (Python 코드 등 긴 문자열 가능)"),
            "overwrite": types.Schema(type="BOOLEAN", description="덮어쓰기 여부 (기본값: False)"),
        },
        required=["filename", "content"],
    ),
)

def main(filename: str, content: str, overwrite: bool = False) -> str:
    # 보안: 상위 디렉토리 접근 제한
    if ".." in filename or filename.startswith("/"):
        return "Error: 현재 디렉토리 및 하위 디렉토리에만 파일을 저장할 수 있습니다."
    
    try:
        # 디렉토리가 없으면 생성
        dirname = os.path.dirname(filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        # 파일 존재 여부 확인 (덮어쓰기가 아닌 경우)
        if os.path.exists(filename) and not overwrite:
            return f"Error: 파일 '{filename}'이(가) 이미 존재합니다. 덮어쓰려면 overwrite=True로 다시 호출해주세요."

        # 파일 저장 (utf-8, 덮어쓰기 모드)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"파일 '{filename}'이(가) 성공적으로 저장되었습니다."
    except Exception as e:
        return f"Error saving file: {e}"

if __name__ == "__main__":
    print(SCHEMA.model_dump_json(indent=2))
