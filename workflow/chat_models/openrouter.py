from workflow.chat_models.llmproviderinterface import LLMProvider
from langchain_openrouter import ChatOpenRouter
import os
from load_dotenv import load_dotenv
load_dotenv()


class OpenRouterProvider(LLMProvider):

    def __init__(self, config):
        self.config = config

    def get_model(self):
        return ChatOpenRouter(
            model=self.config.model,
            temperature=self.config.temperature,
            api_key=os.getenv("OPEN_ROUTER_API_KEY") # pyright: ignore[reportArgumentType]
        )