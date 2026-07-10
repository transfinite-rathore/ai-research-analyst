from ..prompt.intent_prompt import query_analysis_prompt
from ..chat_models.get_model import get_chat_model
from ..graph.structured_output.query_state_output import query_structured_output
import logging

logger = logging.getLogger(__name__)



## Chat Model return structured output from the LLM based on prompt and query
def query_agent(user_query:str):
    try:
        
        llm = get_chat_model().with_structured_output(query_structured_output)
        prompt = query_analysis_prompt.format(user_query=user_query)

        response = llm.invoke(prompt)
        
        
        if response is None:
            logger.exception("No response from query agent!!")
            raise ValueError("Query Agent no response")
        
        logger.info("query agent response success")
        return response

    except Exception as e:
        # print(f"Query Agent Error {e}")
        logger.exception("Query Agent Failed {e}")
    
