from ...utils.models import ResearchOutput,ResearchTask
from workflow.services.news_search import search_news


def news_search(state:ResearchTask):
    """Search about query in latest news."""

    query=state["task"].task_objective
    task_id=state["task"].research_task_id
    parent_task_id=state["task"].parent_task_id
    try:
        result = search_news(query)
        
        output= ResearchOutput(
        task_id=task_id,
        parent_task_id=parent_task_id,
        result=result,
        status="Completed"
        )
    except Exception as e:

        output= ResearchOutput(
        task_id=task_id,
        parent_task_id=parent_task_id,
        result="",
        status="Failed",
        error_message=str(e)
        )
    
    # print(f"news search response {output}")
    return {
  
            "result" :[
           output
        ]
        
    }