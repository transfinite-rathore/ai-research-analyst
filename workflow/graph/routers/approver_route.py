from ..states.analyst_state import AnalystState
from config.latency_tracker import track_time

@track_time
def approval_router(state: AnalystState) -> str:
    status = state.get("approval", {}).get("status")
    return "research_refiner" if status == "rejected" else "report_writer"