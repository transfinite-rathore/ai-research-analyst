from workflow.prompt.research_orch_prompt import research_strategy_prompt
from workflow.chat_models.get_model import get_chat_model
from ..graph.structured_output.research_state_output import ResearchStrategyOutput



def research_agent(task:str):
    try:
        llm = get_chat_model().with_structured_output(ResearchStrategyOutput)
        prompt = research_strategy_prompt.format(tasks=task)
        response = llm.invoke(prompt)
        return response
    except Exception as e :
        print(f"Researcher Agent error {e}")
