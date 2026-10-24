from workflow.chat_models.groq import GroqProvider
from workflow.chat_models.openrouter import OpenRouterProvider
from workflow.chat_models.gemini import GeminiModel
from dataclasses import dataclass

provider_registry = {
    "openrouter": OpenRouterProvider,
    "groq": GroqProvider,
    "gemini":GeminiModel
}

@dataclass
class LLMConfig:
    provider: str
    model: str
    temperature: float

class ChatModelFactory:

    def __init__(self, config: LLMConfig):
        self.config = config

    def get_model(self):
        provider_class = provider_registry.get(
            self.config.provider.lower()
        )

        if provider_class is None:
            raise ValueError(
                f"Unsupported provider: {self.config.provider}"
            )

        provider = provider_class(self.config)

        return provider.get_model()