from langgraph.graph import StateGraph, START, END
import time
from datetime import datetime
from .graph.tools.service_registry import SEARCH_REGISTRY
from .utils.models import ResearchOutput
from .graph.nodes.research_aggregator import aggregate_result
from .graph.states.analyst_state import AnalystState
from .graph.nodes.researcher import research_node
from .graph.routers.task_router import route_task
from config.latency_tracker import track_time
from .graph.tools import (web_search,new_search,paper_search,reddit_search)
from config.config_manager import get_config

MAX_RETRIES=get_config()["searching_retry"]


print("registry id:", id(SEARCH_REGISTRY), "keys:", list(SEARCH_REGISTRY))


@track_time
def search_worker(state: dict):
    task = state["task"]
    fn = SEARCH_REGISTRY.get(task.research_platform)

    def done(status, result="", error=None):
        return {"research": {"result": [ResearchOutput(
            task_id=task.research_task_id,
            parent_task_id=task.parent_task_id,
            research_platform=task.research_platform,
            result=result,
            status=status,
            error_message=error,
            completed_at=datetime.now(),
        )]}}

    if fn is None:
        return done("Failed", error=f"Unknown search tool: {task.research_platform}")

    error = None
    for i in range(MAX_RETRIES):
        try:
            return done("Completed", result=fn(task))
        except Exception as e:
            error = str(e)
            # logger.warning(f"[{task.research_platform}] failed: {error}")
            if i < MAX_RETRIES - 1:
                time.sleep(2 ** i)

    return done("Failed", error=error)




class ResearchGraph:
    RESEARCHER="researcher"
    WORKER="search_worker"
    AGGREGATOR="aggregate_result"
    
    def build(self):
        g = StateGraph(AnalystState)

        g.add_node(self.RESEARCHER, research_node)
        g.add_node(self.WORKER, search_worker)
        g.add_node(self.AGGREGATOR, aggregate_result)

        g.add_edge(START, self.RESEARCHER)
        g.add_conditional_edges(
            self.RESEARCHER,
            route_task,
            path_map=[self.WORKER, self.AGGREGATOR],
        )
        g.add_edge(self.WORKER, self.AGGREGATOR)
        g.add_edge(self.AGGREGATOR, END)

        return g.compile()

