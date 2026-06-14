from load_dotenv import load_dotenv
import os
from langchain_openrouter import ChatOpenRouter
import logging
logger = logging.getLogger(__name__)
load_dotenv()

try:
    chat_model = ChatOpenRouter(
        model="nvidia/nemotron-nano-9b-v2:free",
        temperature=0.8,
        api_key=os.getenv("API_KEY")  # pyright: ignore[reportArgumentType]

        )
    logger.info("LLM Connection successfull!!")
except:
    logger.exception("LLM Failed!")
    raise

def get_chat_model():

    return chat_model