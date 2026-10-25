import logging
from workflow.chat_models.llmfactory import ChatModelFactory
from workflow.chat_models.llmfactory import LLMConfig
from config.config_manager import get_config

logger = logging.getLogger(__name__)

try:

    yaml_config = get_config()["llm"]
    active_provider = yaml_config["active_provider"]

    # Dynamically pulls the nested dictionary for whichever provider is active
    provider_settings = yaml_config[active_provider]

    config = LLMConfig(
        provider=active_provider,
        model=provider_settings["model"],
        temperature=provider_settings["temperature"],
    )
    

    factory = ChatModelFactory(config)

    llm = factory.get_model()
except:
    logger.exception("LLM Failed!")
    raise

def get_chat_model():

    return llm