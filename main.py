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

def main():
    if not (api_key := os.environ.get("GOOGLE_API_KEY")):
        print("Error: GOOGLE_API_KEY not found.")
        return

    # Reset log file at start
    with open("log.md", "w", encoding="utf-8") as f:
        f.write("# Chat Log\n\n")

    genai.configure(api_key=api_key)
    chat = genai.GenerativeModel('gemini-2.0-flash').start_chat(history=[])

    while True:
        try:
            if (msg := input("> ").strip().lower()) in ['quit', 'exit']:
                break
            if msg:
                log_message("User", msg)
                response = chat.send_message(msg).text
                print(response)
                log_message("Gemini", response)
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()