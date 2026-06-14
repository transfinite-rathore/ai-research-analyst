from pydantic import BaseModel
from typing_extensions import List
from ...utils.types import *

class ResearchExecutionPlan(BaseModel):
    parent_task_id: str
    platform: ResearchPlatform
    search_query: str
    reasoning: str

class ResearchStrategyOutput(BaseModel):

    execution_plans: List[
        ResearchExecutionPlan
    ]