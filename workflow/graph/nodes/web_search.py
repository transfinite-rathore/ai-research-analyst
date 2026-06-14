from langchain_community.tools import DuckDuckGoSearchRun
from ...utils.models import ResearchTask,ResearchOutput
from workflow.services.web_search import search_web


def search_query(state:ResearchTask):
    
    """
    Search the query and return the best matching data found

    """

    query = state["task"].task_objective
    task_id=state["task"].research_task_id
    parent_task_id=state["task"].parent_task_id


    try:
        result = search_web(query)
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
    return {
   
            "result" :[
                output
        ]
        
        
    }