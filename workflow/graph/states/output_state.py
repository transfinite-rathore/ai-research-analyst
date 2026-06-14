from pydantic import BaseModel
from typing import Literal


class ReportOutputState(BaseModel):
    title: str
    introduction: str
    executive_summary: str
    main_report: str
    key_takeaways: list[str]
    recommendations: list[str]
    conclusion: str
    markdown_report: str
    report_status: Literal[
        "draft",
        "completed",
        "failed"
    ]