from ..states.analyst_state import AnalystState
import logging
logger = logging.getLogger(__name__)

# def aggregate_results(state: ResearchState):

#     results = state.get("result", [])
#     # print("Aggregator State ",state)
#     aggregated_summary = "\n".join(
#         result.result
#         for result in results
#         if getattr(result, "result", None)
#     )

#     return {
#         "findings": results,
#         "aggregated_summary": aggregated_summary
#     }


def aggregate_result(state: AnalystState):
    research = state.get("research", {})
    outputs = research.get("result", [])

    # task_id -> output (latest wins if a task appears twice)
    by_id = {o.task_id: o for o in outputs}

    # 1. findings (same as before)
    findings, seen = [], set()
    for out in outputs:
        if out.status != "Completed" or not out.result:
            continue
        if out.result in seen:
            continue
        seen.add(out.result)
        findings.append(out.result)

    # 2. mark each search task from its output
    new_search_tasks = []
    for t in research.get("search_tasks", []):
        out = by_id.get(t.research_task_id)
        if out is None:
            new_search_tasks.append(t)            # no result yet: stays Pending
        else:
            new_search_tasks.append(t.model_copy(update={
                "status": out.status,             # Completed or Failed
                "completed_at": out.completed_at,
                "error": out.error_message,
            }))
    logger.info(f"outputs={len(outputs)}, tasks={len(research.get('search_tasks', []))}")
    logger.info(f"ids matched={[t.research_task_id in by_id for t in research.get('search_tasks', [])]}")
    logger.info(f"statuses={[t.status for t in new_search_tasks]}")
    return {"research": {
        "search_tasks": new_search_tasks,
        "findings": findings,
        "aggregated_summary": "\n\n".join(findings),
    }}