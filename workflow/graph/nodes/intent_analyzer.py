import logging
from ..states.analyst_state import AnalystState
from ...agents.query_agent import query_agent
from config.latency_tracker import track_time


logger = logging.getLogger(__name__)

@track_time
def analyze_input(state:AnalystState):
    try:
        logger.info("Entered Analyzer")
        user_query = state["query"]["user_query"]
        response = query_agent(user_query)

        return {
            "query": {
                "user_query":user_query,
                "refined_query": response["refined_query"],
                "topic": response["topic"],
                "research_depth": response.get("research_depth"),
                "explanation_style": response.get("explanation_style")
            }
        }
    except Exception as e:
        logger.exception("Input Analyzer Failed !!",e)