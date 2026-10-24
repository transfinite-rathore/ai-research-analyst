from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time
from datetime import datetime
from .graph.tools.service_registry import SEARCH_REGISTRY
from .utils.models import ResearchOutput
from .graph.nodes.research_aggregator import aggregate_result
from .graph.states.research_state import ResearchState
from .graph.states.analyst_state import AnalystState
from .utils.models import ResearchTask
from .graph.tools.new_search import news_search
from .graph.nodes.researcher import research_node
from .graph.tools.reddit_search import reddit_search
from .graph.tools.paper_search import papers_search
from .graph.tools.web_search import search_query
from .graph.routers.task_router import route_task

MAX_RETRIES=1

#  class ResearchOutput(BaseModel):
#     result: str| list[dict]
#     task_id :str
#     research_platform : Optional[ResearchPlatform]=None
#     parent_task_id :Optional[str]=None 
#     error_message:Optional[str]=None
#     status:Status
#     completed_at : Optional[datetime]=None   

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

# results = state.get("result", [])
#     # print("Aggregator State ",state)
#     aggregated_summary = "\n".join(
#         result.result
#         for result in results
#         if getattr(result, "result", None)
#     )

# def aggregate_result(state: AnalystState):
#     findings, seen = [], set()

#     for out in state.get("research", {}).get("result", []):
#         if out.status != "Completed" or not out.result:
#             continue
#         if out.result in seen:               # skip identical text
#             continue
#         seen.add(out.result)
#         findings.append(out.result)

#     return {"research": {
#         "findings": findings,
#         "aggregated_summary": "\n\n".join(findings),
#     }}

    # return {"research": {"findings": findings, "sources": sources,"aggregated_summary":aggregated_summary}}



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

# graph = StateGraph(ResearchState)


# # =====================================================
# # NODES
# # =====================================================

# graph.add_node(
#     "researcher",
#     research_node
# )

# # graph.add_node(
# #     "route_task",
# #     route_task
# # )

# graph.add_node(
#     "search_worker",
#     search_worker
# )

# graph.add_node(
#     "aggregate_results",
#     aggregate_results
# )

# # # =====================================================
# # # EDGES
# # # =====================================================

# graph.add_edge(
#     START,
#     "researcher"
# )
# graph.add_conditional_edges("researcher",route_task,path_map=["search_worker","aggregate_results"])


# graph.add_edge(
#     "search_worker",
#     "aggregate_results"
# )

# graph.add_edge(
#     "aggregate_results",
#     END
# )

# def route_research(state: ResearchState):

#     sends = []

#     # WEB TASKS
#     for task in state.get("web_search_task", []):

#         sends.append(
#             Send(
#                 "web_search",
#                 {
#                     "task": task
#                 }
#             )
#         )

#     # REDDIT TASKS
#     for task in state.get("reddit_search_task", []):

#         sends.append(
#             Send(
#                 "reddit_search",
#                 {
#                     "task": task
#                 }
#             )
#         )

#     # NEWS TASKS
#     for task in state.get("news_search_task", []):

#         sends.append(
#             Send(
#                 "news_search",
#                 {
#                     "task": task
#                 }
#             )
#         )

#     # PAPER TASKS
#     for task in state.get("paper_search_task", []):

#         sends.append(
#             Send(
#                 "papers_search",
#                 {
#                     "task": task
#                 }
#             )
#         )

#     return sends




# # =====================================================
# # BUILD SUBGRAPH
# # =====================================================

# graph = StateGraph(ResearchState)


# # =====================================================
# # NODES
# # =====================================================

# graph.add_node(
#     "researcher",
#     research_node
# )

# graph.add_node(
#     "web_search",
#     search_query
# )

# graph.add_node(
#     "reddit_search",
#     reddit_search
# )

# graph.add_node(
#     "news_search",
#     news_search
# )

# graph.add_node(
#     "papers_search",
#     papers_search
# )

# graph.add_node(
#     "aggregate_results",
#     aggregate_results
# )


# # =====================================================
# # EDGES
# # =====================================================

# graph.add_edge(
#     START,
#     "researcher"
# )

# graph.add_conditional_edges(
#     "researcher",
#     route_research
# )

# graph.add_edge(
#     "web_search",
#     "aggregate_results"
# )

# graph.add_edge(
#     "reddit_search",
#     "aggregate_results"
# )

# graph.add_edge(
#     "news_search",
#     "aggregate_results"
# )

# graph.add_edge(
#     "papers_search",
#     "aggregate_results"
# )

# graph.add_edge(
#     "aggregate_results",
#     END
# )


# # =====================================================
# # EXPORT
# # =====================================================

# def get_research_graph():

#     return graph