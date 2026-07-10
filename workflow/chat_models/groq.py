from workflow.chat_models.llmproviderinterface import LLMProvider
from langchain_groq import ChatGroq
import os
from load_dotenv import load_dotenv
load_dotenv()

class GroqProvider(LLMProvider):

    def __init__(self, config):
        self.config = config

    def get_model(self):
        return ChatGroq(
            model=self.config.model,
            temperature=self.config.temperature,
            api_key=os.getenv("GROQ_AI_KEY") # pyright: ignore[reportArgumentType]
        )