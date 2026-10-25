from pydantic import BaseModel

class ResumeRequest(BaseModel):
    answer: str
    feedback: str | None = None
    edited_insights: dict | None = None