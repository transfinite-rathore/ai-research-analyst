from ...agents.report_writing_agent import report_writer_agent
from ...graph.states.analyst_state import AnalystState
import logging
from config.latency_tracker import track_time

logger = logging.getLogger(__name__)

@track_time
def report_writer_node(state: AnalystState):
    exp_style = state["query"]["explanation_style"]
    logger.info("")
    report = report_writer_agent(
        original_query=state["query"]["user_query"],
        explanation_style=exp_style,
        research_depth=state["query"]["research_depth"],
        insight=state["insights"],
        evaluation=state["evaluation"],
    )
    logger.info("Report Generation Successful!!")
    return {
        "final_report": report.model_dump()
    }