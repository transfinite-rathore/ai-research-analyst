from typing import TypedDict, Literal
from workflow.utils.models import Insight


class InsightState(TypedDict):
    executive_summary: str
    key_insights: list[Insight]
    limitations: list[str]
    open_questions: list[str]
    conclusion: str
    overall_confidence: Literal["low", "medium", "high"]