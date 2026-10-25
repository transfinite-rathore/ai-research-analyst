from ...utils.models import ResearchTask
from workflow.services.news_search import search_news
from workflow.graph.tools.service_registry import register_search
from config.latency_tracker import track_time

@register_search("news")
@track_time
def news_search(task: ResearchTask) -> str:
    """Search the latest news and return the articles as text."""
    data = search_news(task.search_query)
    articles = data.get("results", [])

    parts = []
    for a in articles:
        content = a.get("content")
        if not content:
            continue
        parts.append(
            f"{a.get('title', 'Untitled')} ({a.get('published_date', 'n/a')})\n"
            f"{content}\n"
            f"Source: {a.get('url', 'n/a')}"
        )

    text = "\n\n".join(parts)

    # no articles found: raise so the worker records a Failed task
    if not text:
        raise ValueError("news search returned no results")

    return text
    
    # print("news  ",data)
    # print("*"*50)
    # articles = data.get("results", [])        # check the real key name
    # return "\n\n".join(a.get("content", "") for a in articles)
    # return search_news(task.search_query)

# @register_search("news")
# def news_search(state:ResearchTask):
#     """Search about query in latest news."""

#     query=state["task"].task_objective
#     task_id=state["task"].research_task_id
#     parent_task_id=state["task"].parent_task_id
#     try:
#         result = search_news(query)
        
#         output= ResearchOutput(
#         task_id=task_id,
#         parent_task_id=parent_task_id,
#         result=result,
#         status="Completed"
#         )
#     except Exception as e:

#         output= ResearchOutput(
#         task_id=task_id,
#         parent_task_id=parent_task_id,
#         result="",
#         status="Failed",
#         error_message=str(e)
#         )
    
#     # print(f"news search response {output}")
#     return {
  
#             "result" :[
#            output
#         ]
        
#     }