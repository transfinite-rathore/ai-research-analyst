from langgraph.types import interrupt
from ..states.analyst_state import AnalystState
from ...utils.mark_status import mark
from config.latency_tracker import track_time
from config.config_manager import get_config

MAX_ROUNDS=get_config()["human_approval_max_iteration"]

@track_time
def verify_human_response(response,rounds):
    if not isinstance(response,dict):
        return None,"",None, "Send response in Dict like {'answer':'yes'}."
    
    answer=response.get("answer","").strip().lower()
    feedbacks=response.get("feedback","").strip()
    edited=response.get("edited_insights")
    
    if answer=="no":
        if rounds>=0:
            return None, "", None, "Review limit reached. Answer 'yes' or 'edit'."
        if not feedbacks:
            return None, "",None ,"A reason ('feedback') is required for 'no'."
    elif answer=="edit":
        if not edited:
            return None, "", None, "'edited_insights' is required for 'edit'."
    if answer!="yes":
        return None, "", None, "'answer' must be 'yes', 'no' or 'edit'."
    return answer,feedbacks,edited,None

def approve(state:AnalystState):
    
    insights=state.get("insights",{})
    approval=state.get("approval",{})
    current_round=approval.get("review_rounds",0)
    evaluation_score=state.get("evaluation",{}).get("content_quality_score",0)
    payload={
        "question":"Are these insights good enough? Should we go for final report generation",
        "insights":insights,
        "evaluation_score":evaluation_score,
        "answer":["yes", "no (needs feedback)", "edit (needs edited_insights)"]
    }
    
    while(True):
        res=interrupt(payload)
        answer,feedback,edited,error=verify_human_response(res,MAX_ROUNDS-current_round)
        if not error:
            break
        payload={**payload,"error":error}
        
    if answer == "yes":
            return {
                "approval": {**approval, "status": "approved", "feedback": ""},
                "planning":mark(state["planning"],"Approver","Completed")    
                    }

    if answer == "edit":
        return {
            "insights": edited,
            "approval": {**approval, "status": "edited", "feedback": "",
                            "original_insights": insights},
            "planning":mark(state["planning"],"Approver","Completed")
        }

    return {  # "no"
        "approval": {**approval, "status": "rejected", "feedback": feedback,
                        "review_rounds": current_round + 1},
        "research_iteration": 1,   # not 0, the researcher treats 0 as the first round
    }