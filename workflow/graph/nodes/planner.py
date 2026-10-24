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
        # print(state)
        refined_user_query = state["query"]["refined_query"]
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

        return {
            "planning": {
                "tasks" : final_task,
                "plan_reasoning": response.reasoning
            }
        }

    except:
        logger.exception("Planning Node Failed!!")
        raise