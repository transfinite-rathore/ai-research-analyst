from .query_state import QueryState
from .evaluation_state import EvaluationState 
from .planning_state import PlanningState
from .research_state import ResearchState 
from .insight_state import InsightState 
from .output_state import ReportOutputState
from .refinement_state import RefinementState
from typing_extensions import TypedDict

class AnalystState(TypedDict):
    query  :QueryState
    planning : PlanningState
    research : ResearchState
    evaluation : EvaluationState
    insights : InsightState
    final_report : ReportOutputState
    refinement:RefinementState
    research_iteration:int