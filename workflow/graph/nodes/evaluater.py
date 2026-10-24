from ..states.analyst_state import AnalystState
from ...agents.evaluationg_agent import evaluation_agent
import logging
from datetime import datetime
from ...utils.mark_status import mark


logger = logging.getLogger(__name__)
def evaluation_node(state:AnalystState):
    # print("Entered Evaluation node")
    logger.info("Evaluation Node")
    query= state["query"]["refined_query"]
    aggregated_summary = state["research"]["aggregated_summary"]
    try:
        evaluation = evaluation_agent(query,aggregated_summary)
        tasks=state["planning"]["tasks"]
 
          
        return {"planning":mark(state["planning"],"Evaluator","Completed"),
            "evaluation":{
                "content_quality_score":evaluation["content_quality_score"],
                "is_insight_ready":evaluation["is_insight_ready"],
                "missing_evidence":evaluation.get("missing_evidence"),
                "contradiction":evaluation.get("contradiction"),
                "evaluation_reasoning":evaluation["evaluation_reasoning"],
                "research_quality" : evaluation["research_quality"],
                "data_coverage" : evaluation["data_coverage"],
                "data_relevance" : evaluation["data_relevance"]
            }
        }
    except Exception:

        return {
            "planning":mark(state["planning"],"Evaluator","Completed"),
            "evaluation": {
                "content_quality_score": 0,
                "is_insight_ready": False,
                "evaluation_reasoning": "Evaluation failed",
            },
                }