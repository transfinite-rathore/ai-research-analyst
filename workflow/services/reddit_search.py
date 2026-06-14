from langchain_community.tools import RedditSearchRun

def search_reddit(query:str):
    try:
        reddit = RedditSearchRun()
        return reddit.run(query)
    except Exception as e:
        return "Error ocurred"+str(e)
# print(search_reddit("quanutm computing"))