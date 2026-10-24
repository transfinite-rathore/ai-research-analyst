from typing_extensions import TypedDict,Optional,List,Annotated
from workflow.utils.models import ResearchTask,Task,ResearchOutput
from ...utils.types import Status
import operator

class ResearchState(TypedDict):
    search_tasks:List[ResearchTask]
    result: List[ResearchOutput]
    
    findings : Optional[List[str]]=None
    sources : Optional[List[str]]=None
    aggregated_summary : Optional[str]=None
    status:Status
    error:Optional[str]=None
    iteration_count: int
    refinement_reason: Optional[str]
    research_history: Optional[List[str]]