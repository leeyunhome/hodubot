# 코드 업데이트 하기 전에 STYLE.md 파일을 참고, 필요하면 STYLE.md 파일 업데이트
import os
import warnings
import datetime
from dotenv import load_dotenv

# Suppress warnings before importing library that emits them
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

load_dotenv()

def log_message(role, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.md", "a", encoding="utf-8") as f:
        f.write(f"### {timestamp} - {role}\n{message}\n\n")

from tools import add_two_numbers, multiply_two_numbers

def main():
    if not (api_key := os.environ.get("GOOGLE_API_KEY")):
        print("Error: GOOGLE_API_KEY not found.")
        return

    # Reset log file at start
    with open("log.md", "w", encoding="utf-8") as f:
        f.write("# Chat Log\n\n")

    genai.configure(api_key=api_key)
    
    # Disable automatic function calling to handle tools manually
    chat = genai.GenerativeModel(
        'gemini-2.0-flash',
        tools=[add_two_numbers, multiply_two_numbers]
    ).start_chat(history=[])

    while True:
        try:
            if (msg := input("호두 > ").strip().lower()) in ['quit', 'exit']:
                break
            if msg:
                log_message("User", msg)
                response = chat.send_message(msg)
                
                # Loop to handle multiple function calls in a row
                while response.candidates[0].content.parts[0].function_call:
                    fc = response.candidates[0].content.parts[0].function_call
                    print(f"AI : 도구 사용 요청 - {fc.name}({fc.args})")
                    log_message("Gemini", str(response)) # Log the request

                    # Manual execution logic
                    result = None
                    if fc.name == 'add_two_numbers':
                        result = add_two_numbers(int(fc.args['a']), int(fc.args['b']))
                    elif fc.name == 'multiply_two_numbers':
                        result = multiply_two_numbers(int(fc.args['a']), int(fc.args['b']))
                    
                    if result is not None:
                        print(f"시스템 : 도구 실행 결과 = {result}")
                        
                        # Send the result back to the model using a dictionary
                        tool_message = {
                            "parts": [
                                {
                                    "function_response": {
                                        "name": fc.name,
                                        "response": {
                                            "result": result,
                                        },
                                    }
                                }
                            ]
                        }
                        log_message("User", f"[도구실행결과] {tool_message}") # Log the tool message immediately after creation
                        response = chat.send_message(tool_message)
                    else:
                        break # Break if unknown tool or execution failed
                
                # Only print text if the response contains text (not another function call)
                if response.candidates[0].content.parts[0].text:
                    print(f"AI : {response.text}")
                log_message("Gemini", str(response))
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()