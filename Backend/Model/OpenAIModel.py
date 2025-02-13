import os
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal 

load_dotenv()

class OutPutFormat(TypedDict):
    """Output format for the chatbot."""
    response: str
    source: Literal["OpenAI"]

class ChatModel:
  def __init__(self) -> None:
    self.openai_chat_client = ChatOpenAI(
      model="gpt-4o-mini",
      api_key=os.environ["OPENAI_API_KEY"]
    )

  def getClient(self) -> ChatOpenAI:
    return self.openai_chat_client
    


