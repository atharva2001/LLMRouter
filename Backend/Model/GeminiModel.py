from langchain_google_genai import ChatGoogleGenerativeAI 
import os
from dotenv import load_dotenv 
from typing import TypedDict, Literal

load_dotenv()

class OutPutFormat(TypedDict):
    """Output format for the chatbot."""
    response: str
    source: Literal["Gemini"]

class ChatModel:
    def __init__(self) -> None:
        self.google_generative_ai_chat_client = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest", 
            google_api_key=os.environ["GOOGLE_API_KEY"]
        )
    
    def getClient(self) -> ChatGoogleGenerativeAI:
        return self.google_generative_ai_chat_client