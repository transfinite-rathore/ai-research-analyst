import logging
from workflow.chat_models.llmfactory import ChatModelFactory
from workflow.chat_models.groq import GroqProvider
from workflow.chat_models.openrouter import OpenRouterProvider
from workflow.chat_models.llmfactory import LLMConfig
from workflow.chat_models.gemini import GeminiModel
logger = logging.getLogger(__name__)

try:
    # provider_registry={
    #     "openrouter": OpenRouterProvider,
    #     "groq": GroqProvider,
    #     "gemini":GeminiModel
    #     # "openai": OpenAIProvider,
    # }
    
#     config = LLMConfig(
#     provider="groq",
#     model="minimaxai/minimax-m2.7",
#     temperature=0,
# )

    config = LLMConfig(
    provider="gemini",
    model="gemini-3.5-flash-lite",
    temperature=0,
)
    # config = LLMConfig(
    #     provider="openrouter",
    #     model="nvidia/nemotron-3.5-super-vl:free",
    #     temperature=0
    # )

    factory = ChatModelFactory(config)

    llm = factory.get_model()
except:
    logger.exception("LLM Failed!")
    raise

def get_chat_model():

    return llm