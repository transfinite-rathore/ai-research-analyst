from pydantic import BaseModel
from typing_extensions import List
from ...utils.types import AgentType
class PlannedTask(BaseModel):
    task:str
    assigned_agent:AgentType

class PlanningTask(BaseModel):
    planned_task: List[PlannedTask]
    reasoning : str