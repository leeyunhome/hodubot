import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
import os

def initialize_model(api_key):
    """
    Initializes the Gemini model with the provided API key.
    """
    genai.configure(api_key=api_key)
    # Using 'gemini-pro' or 'gemini-1.5-flash' as a default model. 
    # Providing generation_config for better control if needed, but keeping it simple for now.
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def start_chat_session(model):
    """
    Starts a new chat session.
    """
    return model.start_chat(history=[])

def send_message(chat_session, message):
    """
    Sends a message to the chat session and returns the response text.
    """
    response = chat_session.send_message(message)
    return response.text
