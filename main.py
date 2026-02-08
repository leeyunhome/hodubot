import os
import sys
import subprocess
import importlib
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
# from tools import load_all_tools  # Deprecated in favor of local load_tools

load_dotenv()

def log(f, role, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"### {timestamp} - {role}\n{message}\n\n")
    f.flush()

def load_tools():
    # list_files.py를 os로 실행하여 tools 폴더의 파일 목록을 받음
    result = subprocess.run([sys.executable, "tools/list_files.py", "tools"], capture_output=True, text=True)
    
    # list_files.py가 ['file1.py', ...] 형태의 문자열을 반환한다고 가정
    filenames = eval(result.stdout.strip())
    
    schemas = []
    functions = {}
    
    for filename in filenames:
        if filename == "__init__.py" or not filename.endswith(".py"):
            continue
            
        module_name = filename[:-3] # .py 제거
        try:
            module = importlib.import_module(f"tools.{module_name}")
            if hasattr(module, "SCHEMA") and hasattr(module, "main"):
                schemas.append(module.SCHEMA)
                functions[module.SCHEMA.name] = module.main
        except Exception as e:
            print(f"Error loading {module_name}: {e}")
            
    return types.Tool(function_declarations=schemas), functions

def main():
    os.system("clear")
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    tools_schema, tool_functions = load_tools()

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            tools=[tools_schema],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True) 
        )
    )
    
    with open("log.md", "a", encoding="utf-8") as f:
        print("호두봇이 시작되었습니다. (종료: quit, exit)")
        while True:
            user_input = input("호두 > ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input:
                continue

            log(f, "User", user_input)

            try:
                response = chat.send_message(user_input)
                log(f, "Gemini", str(response))

                while True:
                    parts = response.candidates[0].content.parts
                    
                    # function_call이 없으면 루프 탈출
                    function_calls = [part.function_call for part in parts if part.function_call]
                    if not function_calls:
                        break
                    
                    response_parts = []
                    
                    for fc in function_calls:
                        fn = tool_functions.get(fc.name)
                        
                        if not fn:
                             result = f"Error: Unknown tool {fc.name}"
                        else:
                            print(f"AI: 도구 실행 - {fc.name}({fc.args})")
                            try:
                                result = fn(**fc.args)
                            except Exception as e:
                                result = f"Error: {e}"
                                
                        print(f"시스템: 결과 - {result}")

                        log(f, "Tool->Gemini", f"[도구 실행 결과] {fc.name}({fc.args}) = {result}")

                        response_parts.append(
                            types.Part.from_function_response(
                                name=fc.name,
                                response={"result": result}
                            )
                        )
                    
                    # 모든 결과를 한 번에 전송
                    response = chat.send_message(response_parts)
                    log(f, "Gemini", str(response))
                
                if response.text:
                    print(f"AI: {response.text}")

            except Exception as e:
                print(f"Error: {e}")
                log(f, "Error", str(e))

if __name__ == "__main__":
    main()