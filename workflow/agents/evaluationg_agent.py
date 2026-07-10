import logging
from workflow.chat_models.get_model import get_chat_model
from workflow.prompt.evaluator_prompt import evaluation_prompt
from ..graph.states.evaluation_state import EvaluationState

logger = logging.getLogger(__name__)


def evaluation_agent(query:str,agg_summary:str):
    try:
        logger.info("Evaluation Agent stated!")
        llm = get_chat_model().with_structured_output(EvaluationState) # type: ignore
        prompt=evaluation_prompt.format(user_query=query,research_findings=agg_summary)
        
        response=llm.invoke(prompt)
        
        if response is None:
            logger.exception("No response from Evaluation agent!!")
            raise ValueError("Evaluation Agent no response")
        logger.info("Evaluation reponse received")
        return response
    
    except Exception as e:
        logger.exception("Evaluation Agent Failed!!",str(e))
        raise e