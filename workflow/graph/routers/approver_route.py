from ..states.analyst_state import AnalystState

def approval_router(state: AnalystState) -> str:
    status = state.get("approval", {}).get("status")
    return "research_refiner" if status == "rejected" else "report_writer"