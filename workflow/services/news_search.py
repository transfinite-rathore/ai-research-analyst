from langchain_tavily import TavilySearch
from load_dotenv import load_dotenv
import os

load_dotenv()
## TESTED OK
def search_news(query:str):
    tool = TavilySearch(
        tavily_api_key=os.getenv("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"),
        max_results=2,
        topic="news"
    )
    result = tool.invoke(query)
    return result

# print(search_news("quantum computing"))