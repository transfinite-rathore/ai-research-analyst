import logging
from langgraph.types import interrupt,Command
from langgraph.errors import GraphInterrupt
from ...agents.planning_agent import planning_agent
from ..states.analyst_state import AnalystState
from ...utils.models import Task
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger(__name__)

def planning_node(state : AnalystState):
    # print("Entered Planner")
    try:
        logger.info("Entered Planner")
        refined_user_query = state["query"]["refined_query"]
        # logger.info(f"refined user query {refined_user_query}")
        response = planning_agent(refined_user_query)
        final_task=[]
        for task in response.planned_task:
            one_task=Task(assigned_agent=task.assigned_agent,
                task_objective=task.task,
                task_id=str(uuid4()),
                status="Pending",
                created_at = datetime.now()
            )
            final_task.append(one_task)
        # decision = interrupt({
        #     "message": "Plans are generated if you like proceed with Yes/No",
        #     "Finalized_task": [
        #         {
        #             "task_id": t.task_id,
        #             "task_objective": t.task_objective,
        #             "assigned_agent": t.assigned_agent,
        #             "status": t.status,
        #         }
        #         for t in final_task
        #     ],
        #     "allowed_actions": ["yes", "no"]
        # })
        # if decision["action"].lower()=="yes":
            
        return {
            "planning": {
                "tasks" : final_task,
                "plan_reasoning": response.reasoning
            }
        }
    #     else:
    #         return Command(
    #             goto="planner"
    #         )
    # except GraphInterrupt:
    #     raise
    except:
        logger.exception("Planning Node Failed!!")
        raise