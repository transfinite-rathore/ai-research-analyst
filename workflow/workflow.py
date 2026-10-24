import logging
import json
import sqlite3
from pathlib import Path
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .graph.states.analyst_state import AnalystState
from .graph.routers.evaluation import evaluation_router
from .graph.routers.approver_route import approval_router
from .graph.nodes.intent_analyzer import analyze_input
from .graph.nodes.planner import planning_node
from .graph.nodes.evaluater import evaluation_node
from .graph.nodes.insight_generator import generate_insight
from .graph.nodes.approver import approve
from .research_subgraph import ResearchGraph
from .graph.nodes.report_writer_node import report_writer_node
from .graph.nodes.research_refinement_node import research_refinement_node
from logging_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjust based on this file's location

DB_DIR = BASE_DIR / "db"/"data"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "ai_analyst_cp.sqlite"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn)

# conn = sqlite3.connect(
#     "ai_analyst.db",
#     check_same_thread=False
# )

# checkpointer=SqliteSaver.from_conn_string(conn)



graph = StateGraph(AnalystState)


research_subgraph = ResearchGraph().build()
sub_png_bytes = research_subgraph.get_graph().draw_mermaid_png()

BASE_DIR = Path(__file__).resolve().parent  # Adjust based on this file's location

SNAPSHOT_DIR = BASE_DIR / "workflow_snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_PATH = SNAPSHOT_DIR / "research_subgraph.png"

with open(GRAPH_PATH, "wb") as f:
    f.write(sub_png_bytes)


class AnalystWorkflow:
    ANALYZE = "analyze_input"
    PLANNER = "planner"
    RESEARCH = "research_phase"
    EVALUATOR = "evaluator"
    REFINER = "research_refiner"
    INSIGHTS = "insight_generator"
    APPROVER = "human_approver"
    REPORT = "report_writer"

    def __init__(
        self,
        checkpointer=None,
        max_research_rounds: int = 3,
        quality_threshold: float = 3.5,
    ):
        self.checkpointer = checkpointer
        self.max_rounds = max_research_rounds
        self._graph = self._build()          # built exactly once

    @property
    def graph(self):
        return self._graph



    def _build(self):
        g = StateGraph(AnalystState)

        g.add_node(self.ANALYZE, analyze_input)
        g.add_node(self.PLANNER, planning_node)
        g.add_node(self.RESEARCH, research_subgraph)
        g.add_node(self.EVALUATOR, evaluation_node)
        g.add_node(self.REFINER, research_refinement_node)
        g.add_node(self.INSIGHTS, generate_insight)
        g.add_node(self.APPROVER,approve)
        g.add_node(self.REPORT, report_writer_node)

        g.add_edge(START, self.ANALYZE)
        g.add_edge(self.ANALYZE, self.PLANNER)
        g.add_edge(self.PLANNER, self.RESEARCH)
        g.add_edge(self.RESEARCH, self.EVALUATOR)
        g.add_conditional_edges(
            self.EVALUATOR,
            evaluation_router,
            {"insights": self.INSIGHTS, "refinement": self.REFINER},
        )
        g.add_edge(self.REFINER, self.RESEARCH)
        g.add_edge(self.INSIGHTS, self.APPROVER)
        g.add_conditional_edges(
            self.APPROVER,
            approval_router,{"refine": self.REFINER, "report": self.REPORT}
            )
        g.add_edge(self.REPORT, END)

        return g.compile(checkpointer=self.checkpointer)

    def run(self, query: str, config:dict):
        # config = {"configurable": {"thread_id": thread_id}}
        state = {"query": {"user_query": query}, "research_iteration": 0}
        return self._graph.invoke(state, config=config)

workflow=AnalystWorkflow()
png_bytes = workflow.graph.get_graph(xray=True).draw_mermaid_png()

# file_path=PATH(__file__)
BASE_DIR = Path(__file__).resolve().parent  # Adjust based on this file's location

SNAPSHOT_DIR = BASE_DIR / "workflow_snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_PATH = SNAPSHOT_DIR / "research_analyst_graph.png"

with open(GRAPH_PATH, "wb") as f:
    f.write(png_bytes)

initial_state = {
    "query": {
        "user_query": "Explain quantum computing"
    },
    "research_iteration": 0
}
config = {
    "configurable": {
        "thread_id": "thread_01"
    }
}

final_state=workflow.run("Explain quantum computing",config)
print(final_state.get("__interrupt__"))                 # should show the insights payload
print(workflow.graph.get_state(config).next) 
# print(final_state)
# print("*"*50)
# print(final_state["final_report"])

with open("final_state101.json", "w", encoding="utf-8") as f:
    json.dump(
        final_state,
        f,
        indent=4,
        default=str
    )
# Router




# =========================================
# WRAPPER NODE
# =========================================

# def run_research_subgraph(state: AnalystState):

#     if state.get("research_iteration", 0) == 0:

#         tasks = [
#             task
#             for task in state["planning"]["tasks"]
#             if task.assigned_agent == "Researcher"
#         ]

#         previous_results = []

#     else:

#         tasks = state.get(
#             "refinement", {}
#         ).get(
#             "tasks",
#             []
#         )

#         previous_results = state.get(
#             "research",
#             {}
#         ).get(
#             "result",
#             []
#         )

#     if not tasks:
#         return {}

#     subgraph_output = research_subgraph.invoke(
#         {
#             "tasks": tasks,
#             "result": previous_results
#         }
#     )

#     return {
#         "research": subgraph_output
#     }


# =========================================
# ADD NODES
# =========================================
# graph.add_node(
#     "analyze_input",
#     analyze_input
# )

# graph.add_node(
#     "planner",
#     planning_node
# )

# graph.add_node(
#     "research_phase",
#     run_research_subgraph
# )
# graph.add_node("evaluator", evaluation_node)
# graph.add_node("insight_generator",generate_insight)
# graph.add_node("report_writer",report_writer_node)
# graph.add_node("research_refiner",research_refinement_node)

# # =========================================
# # EDGES
# # =========================================

# graph.add_edge(
#     START,
#     "analyze_input"
# )

# graph.add_edge(
#     "analyze_input",
#     "planner"
# )

# graph.add_edge(
#     "planner",
#     "research_phase"
# )

# graph.add_edge(
#     "research_phase",
#     "evaluator"
# )
# graph.add_conditional_edges(
#     "evaluator",evaluation_router,{
#         "insights":"insight_generator",
#         "refinement":"research_refiner"
#     }
# )
# graph.add_edge(
#     "research_refiner",
#     "research_phase"
# )

# graph.add_edge(
#     "insight_generator","report_writer"
# )
# graph.add_edge(
#     "report_writer",END
# )

# =========================================
# COMPILE
# =========================================

# workflow = graph.compile(checkpointer=checkpointer)

# with open("workflow_snap_shots\\research_analyst_graph.png", "wb") as f:
#     f.write(png_bytes)

# =========================================
# RUN
# =========================================


# final_state = workflow.invoke(initial_state,config=config)

# snapshot = workflow.get_state(config)

# if snapshot.interrupts:

#     print(snapshot.interrupts)

#     user_input = input("Approve? yes/no: ")

#     result = workflow.invoke(
#         Command(
#             resume={
#                 "action": user_input
#             }
#         ),
#         config=config
#     )

# print(final_state["research"])

# print("\n")
# print("=" * 100)
# print("FINAL STATE")
# print("=" * 100)

# print(final_state["final_report"])

# with open("final_state1.json", "w", encoding="utf-8") as f:
#     json.dump(
#         final_state,
#         f,
#         indent=4,
#         default=str
#     )

