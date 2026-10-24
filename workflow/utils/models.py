from pydantic import BaseModel
from typing_extensions import Optional,List,Literal,TypedDict
from datetime import datetime
from .types import *



class Task(BaseModel):
    task_id : str
    task_objective : str
    status : Status
    created_at: datetime

    assigned_agent : AgentType
    completed_at : Optional[datetime]=None
    source : Optional[List[str]] =None

class ResearchTask(BaseModel):
    research_task_id: str
    parent_task_id: str
    task_objective: str
    research_platform: str
    search_query: str
    status: Status
    created_at: datetime

    # NEW: filled by the worker
    items: list[dict] = []         # [{"url": ..., "summary": ...}]
    error: str | None = None



class ResearchOutput(BaseModel):
    result: str| list[dict]
    task_id :str
    research_platform : Optional[ResearchPlatform]=None
    parent_task_id :Optional[str]=None 
    error_message:Optional[str]=None
    status:Status
    completed_at : Optional[datetime]=None


class Insight(TypedDict):
    insight: str
    evidence: list[str]
    confidence: Literal["low", "medium", "high"]

class OutputArtificat(BaseModel):
    output_id : str
    content : str
    output_format : Optional[OutputFormat]
    target_audience : Optional[AudienceType]
    error_message : Optional[List[str]]
    used_insight_ids: Optional[List[str]] = None
    generated_at : datetime