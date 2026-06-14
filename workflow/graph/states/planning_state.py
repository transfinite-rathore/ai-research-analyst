from typing_extensions import TypedDict,List,Optional
from workflow.utils.models import Task


class PlanningState(TypedDict):
    tasks : List[Task]
    plan_reasoning : str
    replanning_required: Optional[bool] =None