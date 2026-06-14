import logging
from workflow.chat_models.get_model import get_chat_model
from workflow.prompt.report_output_prompt import report_writer_prompt
from ..graph.states.output_state import ReportOutputState
from ..graph.states.insight_state import InsightState
from ..graph.states.evaluation_state import EvaluationState
logger = logging.getLogger(__name__)

llm = get_chat_model().with_structured_output(ReportOutputState)


def report_writer_agent(
    original_query: str,
    explanation_style: str|None,
    research_depth: str | None,
    insight: InsightState,
    evaluation: EvaluationState,
) -> ReportOutputState:
    """
    Generate a human-readable research report from insights.
    """

    try:
        logger.info("Report generated started")
        prompt = report_writer_prompt.format(
            original_query=original_query,
            explanation_style=explanation_style,
            research_depth=research_depth,
            insight=insight,
            evaluation=evaluation,
        )

        response = llm.invoke(prompt)

        logger.info("Report Agent successfull")

        return response

    except Exception as e:
        logger.exception("Report generation failed")
        raise e