from typing import TypedDict

class ApproverState(TypedDict, total=False):
    status: str            # "approved" | "edited" | "rejected"
    feedback: str
    review_rounds: int
    original_insights: dict