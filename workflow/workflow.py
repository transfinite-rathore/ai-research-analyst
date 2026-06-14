import logging
import json
import uuid
import sqlite3
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .graph.states.analyst_state import AnalystState
from .graph.nodes.intent_analyzer import analyze_input
from .graph.nodes.planner import planning_node
from .graph.nodes.evaluater import evaluation_node
from .graph.nodes.insight_generator import generate_insight
from .research_subgraph import get_research_graph
from .graph.nodes.report_writer_node import report_writer_node
from .graph.nodes.research_refinement_node import research_refinement_node
from logging_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

conn = sqlite3.connect("ai_analyst_cp.sqlite", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# conn = sqlite3.connect(
#     "ai_analyst.db",
#     check_same_thread=False
# )

# checkpointer=SqliteSaver.from_conn_string(conn)



graph = StateGraph(AnalystState)

# =========================================
# COMPILED SUBGRAPH
# =========================================

research_subgraph = get_research_graph().compile()
sub_png_bytes = research_subgraph.get_graph().draw_mermaid_png()

with open("research_subgraph.png", "wb") as f:
    f.write(sub_png_bytes)

# Router

MAX_ITERATIONS = 3
QUALITY_THRESHOLD = 4.5

def evaluation_router(state: AnalystState):

    score = state["evaluation"]["content_quality_score"]
    iteration = state.get("research_iteration", 0)
    logger.info(f"iteration count -> {state['research_iteration']}")
    if (
        score <= QUALITY_THRESHOLD
        and iteration < MAX_ITERATIONS
    ):
        logger.info(f"Evaluator decided to refinement with score {score} for iter no {iteration+1}")
        # decision = interrupt({
        #     "evalutaion_score":score,
        #     "evaluation_reasoning":state["evaluation"]["evaluation_reasoning"],
        #     "question":f"Evaluator decided for refinement research should I try refinement Yes/No",
        #     "allowed_actions":["Yes","No"]
        # })
        # if(decision["action"].lower()=="yes"):
        return "refinement"
    logger.info(f"Evaluator decided to inisghts with score {score}")
    return "insights"


# =========================================
# WRAPPER NODE
# =========================================

def run_research_subgraph(state: AnalystState):

    if state.get("research_iteration", 0) == 0:

        tasks = [
            task
            for task in state["planning"]["tasks"]
            if task.assigned_agent == "Researcher"
        ]

        previous_results = []

    else:

        tasks = state.get(
            "refinement", {}
        ).get(
            "tasks",
            []
        )

        previous_results = state.get(
            "research",
            {}
        ).get(
            "result",
            []
        )

    if not tasks:
        return {}

    subgraph_output = research_subgraph.invoke(
        {
            "tasks": tasks,
            "result": previous_results
        }
    )

    return {
        "research": subgraph_output
    }


# =========================================
# ADD NODES
# =========================================

graph.add_node(
    "analyze_input",
    analyze_input
)

graph.add_node(
    "planner",
    planning_node
)

graph.add_node(
    "research_phase",
    run_research_subgraph
)
graph.add_node("evaluator", evaluation_node)
graph.add_node("insight_generator",generate_insight)
graph.add_node("report_writer",report_writer_node)
graph.add_node("research_refiner",research_refinement_node)

# =========================================
# EDGES
# =========================================

graph.add_edge(
    START,
    "analyze_input"
)

graph.add_edge(
    "analyze_input",
    "planner"
)

graph.add_edge(
    "planner",
    "research_phase"
)

graph.add_edge(
    "research_phase",
    "evaluator"
)
graph.add_conditional_edges(
    "evaluator",evaluation_router,{
        "insights":"insight_generator",
        "refinement":"research_refiner"
    }
)
graph.add_edge(
    "research_refiner",
    "research_phase"
)

graph.add_edge(
    "insight_generator","report_writer"
)
graph.add_edge(
    "report_writer",END
)

# =========================================
# COMPILE
# =========================================

workflow = graph.compile(checkpointer=checkpointer)
png_bytes = workflow.get_graph().draw_mermaid_png()

with open("research_analyst_graph.png", "wb") as f:
    f.write(png_bytes)

# =========================================
# RUN
# =========================================

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
final_state = workflow.invoke(initial_state,config=config)

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

