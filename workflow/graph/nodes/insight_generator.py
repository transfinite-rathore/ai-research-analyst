import logging
from ..states.analyst_state import AnalystState
from ...agents.insight_genertor_agent import insight_agent
from config.latency_tracker import track_time
logger = logging.getLogger(__name__)

@track_time
def generate_insight(state:AnalystState):
    try:
        logger.info("Inside Generating Insights")
        
        original_query=state["query"]["user_query"]
        research_depth=state["query"]["research_depth"]
        expalanation_style=state["query"]["explanation_style"]
        refined_query=state["query"]["refined_query"]
        summary=state["research"]["aggregated_summary"]
        
        insight = insight_agent(original_query,research_depth,expalanation_style,refined_query,summary)
        
        logger.info("Respone gathered , returing insigts")
        return {
        "insights": insight}
        
        
    except :
        logger.exception("Insight generator failed")
        raise