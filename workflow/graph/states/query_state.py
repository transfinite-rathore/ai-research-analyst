from typing_extensions import TypedDict,Literal,Optional
from ...utils.models import AudienceType
class QueryState(TypedDict):
    user_query : str
    refined_query : Optional[str]
    topic: Optional[str]
    research_depth : Optional[Literal["Beginner","Intermediate","Expert"]]
    explanation_style : Optional[AudienceType]