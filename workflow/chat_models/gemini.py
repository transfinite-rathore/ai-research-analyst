import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .llmproviderinterface import LLMProvider

load_dotenv()


class GeminiModel(LLMProvider):
    
    def __init__(self,config):
        self.config=config
    
    def get_model(self):
        return ChatGoogleGenerativeAI(
            model=self.config.model,
            temperature=self.config.temperature,
            api_key=os.getenv("GEMINI_API_KEY") # pyright: ignore[reportArgumentType]
        )
