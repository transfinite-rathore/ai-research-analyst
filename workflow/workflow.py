import logging
from pathlib import Path
from langgraph.graph import StateGraph, START, END
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
from config.latency_tracker import start_telemetry

setup_logger()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjust based on this file's location
print(str(BASE_DIR)+"logs/node_times.jsonl")
start_telemetry(str(BASE_DIR)+"/logs/node_times_prl2.jsonl")
# DB_DIR = BASE_DIR / "db"/"data"
# DB_DIR.mkdir(exist_ok=True)

# DB_PATH = DB_DIR / "ai_analyst_cp.sqlite"

# conn = sqlite3.connect(DB_PATH, check_same_thread=False)
# checkpointer = SqliteSaver(conn)

# conn = sqlite3.connect(
#     "ai_analyst.db",
#     check_same_thread=False
# )

# checkpointer=SqliteSaver.from_conn_string(conn)



graph = StateGraph(AnalystState)


research_subgraph = ResearchGraph().build()
# sub_png_bytes = research_subgraph.get_graph().draw_mermaid_png()

# BASE_DIR = Path(__file__).resolve().parent  # Adjust based on this file's location

# SNAPSHOT_DIR = BASE_DIR / "workflow_snapshots"
# SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# GRAPH_PATH = SNAPSHOT_DIR / "research_subgraph.png"

# with open(GRAPH_PATH, "wb") as f:
#     f.write(sub_png_bytes)


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
    ):
        self.checkpointer = checkpointer
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
            approval_router,{"research_refiner": self.REFINER, "report_writer": self.REPORT}
            )
        g.add_edge(self.REPORT, END)

        return g.compile(checkpointer=self.checkpointer)

    def run(self, query: str, config:dict):
        # config = {"configurable": {"thread_id": thread_id}}
        state = {"query": {"user_query": query}, "research_iteration": 0}
        return self._graph.invoke(state, config=config)

workflow=AnalystWorkflow()
# png_bytes = workflow.graph.get_graph(xray=True).draw_mermaid_png()

# # file_path=PATH(__file__)
# BASE_DIR = Path(__file__).resolve().parent  # Adjust based on this file's location

# SNAPSHOT_DIR = BASE_DIR / "workflow_snapshots"
# SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# GRAPH_PATH = SNAPSHOT_DIR / "research_analyst_graph.png"

# with open(GRAPH_PATH, "wb") as f:
#     f.write(png_bytes)

# initial_state = {
#     "query": {
#         "user_query": "Explain quantum computing"
#     },
#     "research_iteration": 0
# }
# config = {
#     "configurable": {
#         "thread_id": "thread_01"
#     }
# }

# final_state=workflow.run("Explain quantum computing",config)


# with open("final_state101.json", "w", encoding="utf-8") as f:
#     json.dump(
#         final_state,
#         f,
#         indent=4,
#         default=str
#     )
