from ...utils.models import ResearchTask,ResearchOutput
from workflow.services.paper_search import search_paper
from workflow.graph.tools.service_registry import register_search

@register_search("research_paper")
def papers_search(task: ResearchTask) -> str:
    """Search academic papers."""
    results = search_paper(task.search_query)
    return "\n\n".join(r["summary"] for r in results)


# @register_search("research_paper")
# def papers_search(state:ResearchTask):
#     """Search academic papers."""

#     query=state["task"].task_objective
#     task_id=state["task"].research_task_id
#     parent_task_id=state["task"].parent_task_id


#     try:
#         result = search_paper(query)
#         # print("#"*100)
#         # print("arvic ",result)
#         # print("#"*100)
#         combined_result = "\n\n".join(
#             res["summary"] for res in result
#         )
#         output= ResearchOutput(
#         task_id=task_id,
#         parent_task_id=parent_task_id,
#         result=combined_result,
#         status="Completed"
#         )
        
#     except Exception as e:
        
#         output= ResearchOutput(
#                 task_id=task_id,
#                 parent_task_id=parent_task_id,
#                 result="",
#                 status="Failed",
#                 error_message=str(e)
#                 )
#     # print(f"paper search response {output}")
#     return {
      
#             "result" :[
#                 output
          
#         ]
        
    # }
