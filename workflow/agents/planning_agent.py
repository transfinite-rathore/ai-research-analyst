from workflow.prompt.intent_prompt import query_analysis_prompt
from workflow.chat_models.get_model import get_chat_model
from ..graph.structured_output.planning_state_output import PlanningTask



def planning_agent(refined_user_query:str|None):
    try:
        llm = get_chat_model().with_structured_output(PlanningTask)
        response = llm.invoke(refined_user_query)
        # print("PLanning reposne ",response)
        return response
    except Exception as e:
        print(f"Planning Agent Error {e}")

