# 코드 업데이트 하기 전에 STYLE.md 파일을 참고, 필요하면 STYLE.md 파일 업데이트
import os
import warnings
import datetime
import importlib
import pkgutil
import sys
from dotenv import load_dotenv
import tools

# Suppress warnings before importing library that emits them
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

load_dotenv()

def log_message(role, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.md", "a", encoding="utf-8") as f:
        f.write(f"### {timestamp} - {role}\n{message}\n\n")

def load_tools():
    """Dynamically loads tools from the tools directory."""
    loaded_tools = []
    tool_functions = {}
    
    # Reload the tools package to pick up new files
    importlib.reload(tools)
    
    # tools is a namespace package now if __init__.py is gone, or just a directory
    # Better way: get the directory of main.py and join with 'tools'
    path = os.path.join(os.path.dirname(__file__), 'tools')
    
    for _, name, _ in pkgutil.iter_modules([path]):
        if name == "__init__":
            continue
            
        module_name = f"tools.{name}"
        
        # Check if module is already loaded, if so reload it
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
            
        # Inspect module for functions that match the tool pattern (simple check for now)
        # We assume the function name matches the file name for simplicity, or just load everything callable that isn't private
        # Better: Load the specific function that matches the module name?
        # Or just look for the function with the same name as the module
        if hasattr(module, name):
            func = getattr(module, name)
            if callable(func):
                loaded_tools.append(func)
                tool_functions[name] = func
                print(f"Loaded tool: {name}")

    return loaded_tools, tool_functions

def main():
    if not (api_key := os.environ.get("GOOGLE_API_KEY")):
        print("Error: GOOGLE_API_KEY not found.")
        return

    # Reset log file at start
    with open("log.md", "w", encoding="utf-8") as f:
        f.write("# Chat Log\n\n")

    genai.configure(api_key=api_key)
    
    # Initial Tool Load
    current_tools, tool_map = load_tools()
    
    # Disable automatic function calling to handle tools manually
    chat = genai.GenerativeModel(
        'gemini-2.0-flash',
        tools=current_tools
    ).start_chat(history=[])

    while True:
        try:
            msg = input("호두 > ").strip().lower()
            
            if msg in ['quit', 'exit']:
                break
            
            if msg == '/reload':
                print("Reloading tools...")
                current_tools, tool_map = load_tools()
                # Re-initialize the chat model with new tools. History is preserved manually if needed, 
                # but technically start_chat creates a new session. 
                # To keep history, we can pass the old history.
                old_history = chat.history
                chat = genai.GenerativeModel(
                    'gemini-2.0-flash',
                    tools=current_tools
                ).start_chat(history=old_history)
                print("Tools reloaded.")
                continue

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
                    if fc.name in tool_map:
                        try:
                            # Extract arguments safely
                            args = {key: value for key, value in fc.args.items()}
                            result = tool_map[fc.name](**args)
                        except Exception as e:
                            print(f"Error executing tool {fc.name}: {e}")
                            result = f"Error: {e}"
                    else:
                        print(f"Error: Tool {fc.name} not found.")
                        break

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
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()