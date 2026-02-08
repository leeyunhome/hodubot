import os
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools import load_all_tools 

load_dotenv()

def log(f, role, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"### {timestamp} - {role}\n{message}\n\n")
    f.flush()

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    tools_schema, tool_functions = load_all_tools()

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            tools=tools_schema,
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

                # 도구 호출이 연속적으로 발생할 수 있으므로 반복 처리
                while True:
                    part = response.candidates[0].content.parts[0]
                    
                    # function_call이 없으면 루프 탈출
                    if not part.function_call:
                        break
                    
                    fc = part.function_call
                    fn = tool_functions.get(fc.name)
                    
                    if not fn:
                         print(f"Error: Unknown tool {fc.name}")
                         break
                         
                    print(f"AI: 도구 실행 - {fc.name}({fc.args})")
                    
                    # 실행
                    try:
                        result = fn(**fc.args)
                    except Exception as e:
                        result = f"Error: {e}"
                        
                    print(f"시스템: 결과 - {result}")

                    # 결과 전송
                    response = chat.send_message(
                        types.Part.from_function_response(
                            name=fc.name,
                            response={"result": result}
                        )
                    )
                    log(f, "Gemini", str(response))
                
                if response.text:
                    print(f"AI: {response.text}")

            except Exception as e:
                print(f"Error: {e}")
                log(f, "Error", str(e))

if __name__ == "__main__":
    main()