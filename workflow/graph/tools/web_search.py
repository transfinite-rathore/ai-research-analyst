from langchain_community.tools import DuckDuckGoSearchRun
from ...utils.models import ResearchTask,ResearchOutput
from workflow.services.web_search import search_web
from datetime import datetime
from ...utils.types import ResearchPlatform
from workflow.graph.tools.service_registry import register_search

@register_search("websearch")
def search_query(task: ResearchTask) -> str:
    """Search the web and return the best matching data."""
    return search_web(task.search_query)

# @register_search("websearch")
# def search_query(state:ResearchTask):
    
#     """
#     Search the query and return the best matching data found

#     """

#     query = state["task"].task_objective
#     task_id=state["task"].research_task_id
#     parent_task_id=state["task"].parent_task_id


#     try:
#         result = search_web(query)
        
#         output= ResearchOutput(
#         task_id=task_id,
#         parent_task_id=parent_task_id,
#         result=result,
#         research_platform=ResearchPlatform["news"],
#         status="Completed",
#         completed_at=datetime.now()
#         )
#     except Exception as e:
        
#         output= ResearchOutput(
#         task_id=task_id,
#         parent_task_id=parent_task_id,
#         result="",
#         research_platform=ResearchPlatform["news"],
#         status="Failed",
#         error_message=str(e)
#          )
#     return {
   
#             "result" :[
#                 output
#         ]
        
        
#     }