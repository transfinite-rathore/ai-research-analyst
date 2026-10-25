from ..states.analyst_state import AnalystState
from langgraph.types import Send
from config.latency_tracker import track_time

from langchain_core.runnables import RunnableConfig

# @track_time
# def route_task(state: AnalystState, config: RunnableConfig):
#     tasks = state.get("research", {}).get("search_tasks", [])
#     if not tasks:
#         return "aggregate_results"

#     mode = config.get("configurable", {}).get("research_mode", "parallel")
#     if mode == "sequential":
#         return [Send("search_worker", {"tasks": tasks})]    # one worker, loops over all
#     return [Send("search_worker", {"task": t}) for t in tasks]


@track_time
def route_task(state:AnalystState):
    tasks=state.get("research",{}).get("search_tasks",[])
    send=[Send("search_worker",{"task":t}) for t in tasks]
    return send or "aggregate_result"