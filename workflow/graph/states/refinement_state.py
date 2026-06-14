from typing import List
from workflow.utils.models import Task
from pydantic import BaseModel


class RefinementState(BaseModel):
    tasks:List[Task]