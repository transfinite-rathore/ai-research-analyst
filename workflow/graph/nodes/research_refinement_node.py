import logging
from ...graph.states.analyst_state import AnalystState
from ...agents.research_refinement_agent import research_refinement_agent

logger= logging.getLogger(__name__)

def research_refinement_node(state: AnalystState):
    try:
        logger.info("Entered Research Refinement")

        evaluation = state["evaluation"]
        query = state["query"]
        research = state["research"]

        strategy_response = research_refinement_agent(
            original_query=query["user_query"],
            tasks=research["tasks"],
            summary=research["aggregated_summary"],
            evaluation=evaluation
        )

        return {
            "refinement":{"tasks":strategy_response.tasks},
            "research_iteration":state["research_iteration"]+1
           
        }

    except:
        logger.exception(
            "Research Refinement Failed"
        )
        raise