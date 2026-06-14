import logging
from ..states.analyst_state import ResearchState
from ...agents.research_strategy_agent import research_agent
from ...utils.types import *
from ...utils.models import ResearchTask
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger(__name__)

def research_node(state: ResearchState):
    try:
        # print("Entered Researcher")
        logger.info("Entered Researcher")
        tasks = state["tasks"]

        formatted_tasks = ""

        for task in tasks:

            formatted_tasks += f"""
            Task ID: {task.task_id}
            Objective: {task.task_objective}
            """

        strategy_response = research_agent(
            formatted_tasks
        )
        # logger.info("Research Agent response ",strategy_response)
        web_search_tasks = []

        reddit_search_tasks = []

        news_search_tasks = []

        paper_search_tasks = []

        # Faster lookup
        task_map = {
            task.task_id: task
            for task in tasks
        }

        for plan in strategy_response.execution_plans:

            parent_task = task_map.get(
                plan.parent_task_id
            )

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

            if plan.platform == "websearch":

                web_search_tasks.append(
                    research_task
                )

            elif plan.platform == "reddit":

                reddit_search_tasks.append(
                    research_task
                )

            elif plan.platform == "news":

                news_search_tasks.append(
                    research_task
                )

            elif plan.platform == "Research Paper":

                paper_search_tasks.append(
                    research_task
                )

        return {

            "web_search_task":
                web_search_tasks,

            "reddit_search_task":
                reddit_search_tasks,

            "news_search_task":
                news_search_tasks,

            "paper_search_task":
                paper_search_tasks
        }
    except:
        logger.exception("Researcher Failed")
        raise

