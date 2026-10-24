from .query_state import QueryState
from .evaluation_state import EvaluationState 
from .planning_state import PlanningState
from .research_state import ResearchState 
from .insight_state import InsightState 
from .output_state import ReportOutputState
from .refinement_state import RefinementState
from .approver_state import ApproverState
from typing_extensions import TypedDict
from typing import Annotated
def merge_result(old:dict,new:dict):
    merged=dict(old or {})
    
    for key,val in dict(new or {}).items():
        if key=="result":
            existing=merged.get("result",[])
            seen={r.task_id for r in existing}
            
            for t in val:
                if t.task_id not in seen:
                    existing.append(t)
                    seen.add(t.task_id)
                    
            merged["result"]=existing
        else:
            merged[key]=val
    return merged

class AnalystState(TypedDict):
    query  :QueryState
    planning : PlanningState
    research : Annotated[ResearchState,merge_result]
    evaluation : EvaluationState
    insights : InsightState
    final_report : ReportOutputState
    refinement:RefinementState
    approval:ApproverState
    research_iteration:int