from langchain_community.tools import DuckDuckGoSearchRun

# TESTED OK
def search_web(query:str):
    search = DuckDuckGoSearchRun()
    result = search.run(query)
    
    return result
    
# print(search_web("total states in India"))
    