import logging
from workflow.chat_models.llmfactory import ChatModelFactory
from workflow.chat_models.groq import GroqProvider
from workflow.chat_models.openrouter import OpenRouterProvider
from workflow.chat_models.llmfactory import LLMConfig

logger = logging.getLogger(__name__)

try:
    provider_registry={
        "openrouter": OpenRouterProvider,
        "groq": GroqProvider,
        # "openai": OpenAIProvider,
    }
    
#     config = LLMConfig(
#     provider="groq",
#     model="llama-3.3-70b",
#     temperature=0,
# )
    config = LLMConfig(
        provider="openrouter",
        model="nvidia/nemotron-nano-9b-v2:free",
        temperature=0
    )

    factory = ChatModelFactory(config)

    llm = factory.get_model()
except:
    logger.exception("LLM Failed!")
    raise

def get_chat_model():

    return llm