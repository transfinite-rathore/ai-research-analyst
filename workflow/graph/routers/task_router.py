from ..states.analyst_state import AnalystState
from langgraph.types import Send

def route_task(state:AnalystState):
    tasks=state.get("research",{}).get("search_tasks",[])
    send=[Send("search_worker",{"task":t}) for t in tasks]
    return send or "aggregate_result"