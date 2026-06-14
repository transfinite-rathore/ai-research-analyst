from typing_extensions import TypedDict,Optional,List,Annotated
from workflow.utils.models import ResearchTask,Task
import operator

class ResearchState(TypedDict):
    tasks: List[Task]
    web_search_task: List[ResearchTask]
    reddit_search_task: List[ResearchTask]
    news_search_task: List[ResearchTask]
    paper_search_task: List[ResearchTask]

    result: Annotated[list, operator.add]
    completed_research_tasks :  Optional[List[ResearchTask]]=None
    failed_research_tasks : Optional[List[ResearchTask]]=None
    findings : Optional[List[str]]=None
    sources : Optional[List[str]]=None
    aggregated_summary : Optional[str]=None
    
    iteration_count: int
    refinement_reason: Optional[str]
    research_history: Optional[List[str]]