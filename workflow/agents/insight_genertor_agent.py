import logging
from workflow.chat_models.get_model import get_chat_model
from workflow.prompt.insight_generator_prompt import insight_prompt
from ..graph.states.insight_state import InsightState
from config.latency_tracker import track_time

logger = logging.getLogger(__name__)
@track_time
def insight_agent(original_query, refined_query,explanation_style,research_depth, summary):
    try:
        logger.info("Inside Insight Agent ")
        prompt = prompt = insight_prompt.format(
        original_query=original_query,
        refined_query=refined_query,
        explanation_style=explanation_style,
        research_depth=research_depth,
        summary=summary
        )
        logger.info("Invoking LLM")
        llm = get_chat_model().with_structured_output(InsightState)
        

        response=llm.invoke(prompt)
        if response is None:
            logger.exception("No response from insight agent!!")
            raise ValueError("Insight Agent no response")
        logger.info("Insight reponse received")
        return response
    except Exception as e:
        logger.exception(f"Insight Agent failed {e}")
        raise e
