from ..states.analyst_state import AnalystState
from ...agents.query_agent import query_agent
import logging

logger = logging.getLogger(__name__)

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
    except:
        logger.exception("Input Analyzer Failed !!")