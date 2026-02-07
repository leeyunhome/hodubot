# 코드 업데이트 하기 전에 STYLE.md 파일을 참고, 필요하면 STYLE.md 파일 업데이트

import os
import sys
from dotenv import load_dotenv
import chat_utils

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        print("Please add your API key to the .env file.")
        sys.exit(1)

    try:
        model = chat_utils.initialize_model(api_key)
        chat = chat_utils.start_chat_session(model)
        
        while True:
            try:
                user_input = input("> ").strip()
            except EOFError:
                break
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue

            try:
                # Ensure we handle potential errors during generation
                response = chat_utils.send_message(chat, user_input)
                print(response)
            except Exception as e:
                print(f"\nAn error occurred: {e}")

    except Exception as e:
        print(f"Failed to initialize chat: {e}")

if __name__ == "__main__":
    main()