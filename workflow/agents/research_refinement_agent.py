import logging
from workflow.prompt.research_refinement_prompt import research_refinement_prompt
from workflow.chat_models.get_model import get_chat_model
from ..utils.models import ResearchTask
from ..graph.states.refinement_state import RefinementState
from ..graph.states.evaluation_state import EvaluationState
from config.latency_tracker import track_time

logger = logging.getLogger(__name__)
@track_time
def research_refinement_agent(
            original_query:str,
            tasks:ResearchTask,
            summary:str,
            evaluation:EvaluationState):
    try:
        llm = get_chat_model().with_structured_output(RefinementState)
        prompt = research_refinement_prompt.format(original_query=original_query,
                                                   tasks=tasks,
                                                   aggregated_summary=summary,
                                                   content_quality_score=evaluation["content_quality_score"],
                                                   missing_evidence=evaluation["missing_evidence"],
                                                   contradiction=evaluation["contradiction"],
                                                   evaluation_reasoning=evaluation["evaluation_reasoning"]
                                                   )
        response = llm.invoke(prompt)
        if response is None:
            raise ValueError(
                "Refinement agent returned None"
            )
        return response
    except Exception as e :
        logger.exception("Refinement Agent Failed!!")
        raise e
