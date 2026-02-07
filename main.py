# 코드 업데이트 하기 전에 STYLE.md 파일을 참고, 필요하면 STYLE.md 파일 업데이트

import os
import sys
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        print("Please add your API key to the .env file.")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        chat = model.start_chat(history=[])
        
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
                response = chat.send_message(user_input)
                print(response.text)
            except Exception as e:
                print(f"\nAn error occurred: {e}")

    except Exception as e:
        print(f"Failed to initialize chat: {e}")

if __name__ == "__main__":
    main()