from datetime import datetime
from ..graph.states.planning_state import PlanningState


def mark(planning: PlanningState, agent: str, status: str) -> dict:
    new_tasks = [
        t.model_copy(update={"status": status, "completed_at": datetime.now()})
        if t.assigned_agent == agent else t
        for t in planning["tasks"]
    ]
    return {**planning, "tasks": new_tasks}