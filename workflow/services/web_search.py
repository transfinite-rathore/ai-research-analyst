from langchain_community.tools import DuckDuckGoSearchRun
from config.latency_tracker import track_time
# TESTED OK
@track_time
def search_web(query:str):
    search = DuckDuckGoSearchRun()
    result = search.run(query)
    
    return result
    
