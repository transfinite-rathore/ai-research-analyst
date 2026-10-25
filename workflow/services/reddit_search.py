from langchain_community.tools import RedditSearchRun
from config.latency_tracker import track_time
@track_time
def search_reddit(query:str):
    try:
        reddit = RedditSearchRun()
        return reddit.run(query)
    except Exception as e:
        return "Error ocurred"+str(e)
# print(search_reddit("quanutm computing"))