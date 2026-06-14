from typing_extensions import Literal,Optional,TypedDict
from ...utils.types import AudienceType

class query_structured_output(TypedDict):
    refined_query : str
    topic: str
    research_depth : Optional[Literal["Beginner","Intermediate","Expert"]]
    explanation_style : Optional[AudienceType]