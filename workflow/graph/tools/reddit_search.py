from ...utils.models import ResearchTask,ResearchOutput
from workflow.services.reddit_search import search_reddit
from workflow.graph.tools.service_registry import register_search


@register_search("reddit")
def reddit_search(task: ResearchTask) -> str:
    """Search Reddit discussions."""
    return search_reddit(task.search_query)

# @register_search("reddit")
# def reddit_search(state:ResearchTask):
#     """Search Reddit discussions."""

#     query=state["task"].task_objective
#     task_id=state["task"].research_task_id
#     parent_task_id=state["task"].parent_task_id


#     try:
#         result = search_reddit(query)
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
#          )
#     # print(f"reddit search response {output}")
#     return {
    
#             "result" :[
#                     output    
#         ]
        
#     }