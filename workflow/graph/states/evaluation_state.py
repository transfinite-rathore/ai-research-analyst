from typing_extensions import Optional,List,TypedDict,Literal
from pydantic import BaseModel,Field

class EvaluationState(TypedDict):
    content_quality_score : int = Field(le=5,ge=0)
    is_insight_ready : bool
    missing_evidence : Optional[str]
    contradiction : Optional[str]
    evaluation_reasoning : str
    research_quality : int = Field(le=5,ge=0)
    data_coverage : Literal["partial","sufficent","comprehensive"]
    data_relevance : Literal["low","medium","high"]

