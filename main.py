import os
import warnings

# Suppress warnings before importing library that emits them
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

def main():
    if not (api_key := os.getenv("GOOGLE_API_KEY")):
        print("Error: GOOGLE_API_KEY not found.")
        return

    genai.configure(api_key=api_key)
    chat = genai.GenerativeModel('gemini-2.0-flash').start_chat(history=[])

    while True:
        try:
            if (msg := input("> ").strip().lower()) in ['quit', 'exit']:
                break
            if msg:
                print(chat.send_message(msg).text)
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()