from ..states.research_state import ResearchState 

def aggregate_results(state: ResearchState):

    results = state.get("result", [])

    aggregated_summary = "\n".join(
        result.result
        for result in results
        if getattr(result, "result", None)
    )

    return {
        "findings": results,
        "aggregated_summary": aggregated_summary
    }