import logging
from ..states.analyst_state import AnalystState
from ...agents.research_strategy_agent import research_agent
from ...utils.types import *
from ...utils.models import ResearchTask
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger(__name__)

def research_node(state: AnalystState):
    try:
        # print("Entered Researcher")
        logger.info("Entered Researcher")
        tasks = [i for i in state["planning"]["tasks"] if i.assigned_agent=="Researcher"]

        formatted_tasks = ""

        for task in tasks:
            formatted_tasks += f" Task ID: {task.task_id} Objective: {task.task_objective}"

        strategy_response = research_agent( formatted_tasks )
        search_task=[]
        # Faster lookup
        task_map = { task.task_id: task for task in tasks }

        for plan in strategy_response.execution_plans:
            parent_task = task_map.get( plan.parent_task_id ) 

            if not parent_task:
                continue

            research_task = ResearchTask(
                research_task_id=str(uuid4()),
                parent_task_id=parent_task.task_id,
                task_objective=parent_task.task_objective,
                research_platform=plan.platform,
                search_query=plan.search_query,
                status="Pending",
                created_at=datetime.now()
            )

            search_task.append(research_task)

        return {
            "research":{
                 "search_tasks":search_task
            }
           
        }
    except Exception:
        logger.exception("Researcher Failed")
        raise

