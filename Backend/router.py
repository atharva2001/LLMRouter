from Model import OpenAIModel, GeminiModel
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
import logging
from typing import TypedDict, Literal
from langchain_core.runnables.base import RunnableLambda 
from operator import itemgetter
from Prompts import gemini_prompt, openai_prompt, route_prompt

class RouteQuery(TypedDict):
    """Route query to the destination."""
    destination: Literal["complex", "medical"]

class Router:
    def __init__(self):
        self.open_ai = OpenAIModel.ChatModel().getClient()
        self.gemini_ai = GeminiModel.ChatModel().getClient()

        open_ai_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are a chatbot that performs complex tasks and computational task.
                            Your task is to resolve user query in simple human understandable plain english.
                            Your Output must be in below format:
                            
                            
                                Reponse: Your Response,
                                Source: OpenAI
                            
                            
                            """),
                ("human", "{query}")
            ]
        )

        gemini_ai_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are a chatbot that performs medical tasks and related work.
                            Your task is to resolve user query in simple human understandable plain english.
                            Your Output must be in below format:
                            
                            
                                Reponse: Your Response,
                                Source: Gemini
                            
                            
                        """),
                ("human", "{query}")
            ]
        )

        self.gemini_ai_chain = gemini_ai_prompt | self.gemini_ai | StrOutputParser()
        self.open_ai_chain = open_ai_prompt | self.open_ai | StrOutputParser()

    def runrouters(self, input_query: str):
        
        logging.basicConfig(level=logging.INFO)
        route_system = "You are an AI bot that route the user query into two categories: complex and medical."
        route_prompts = ChatPromptTemplate.from_messages(
            [
                ("system", route_system),
                ("human", "{query}"),
            ]
        )

        route_chain = (
            route_prompts | 
            self.open_ai.with_structured_output(RouteQuery) | 
            itemgetter("destination")
        )

        chain = {
            "destination": route_chain,
            "query": lambda x: x["query"],

        } | RunnableLambda(
            lambda x: self.open_ai_chain if x["destination"] == "complex" else self.gemini_ai_chain
        )

        try:
            result = chain.invoke({"query": input_query})
            logging.info(f"Result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error: {e}")
            return e



