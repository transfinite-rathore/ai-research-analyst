from typing_extensions import Literal

AgentType=Literal["Evaluator","Researcher","Approver"]
Status=Literal["Pending","Running","Completed","Failed"]
ResearchPlatform = Literal["websearch","reddit","news","Research Paper"]
OutputFormat = Literal["markdown", "summary","technical_report", "bullet_points", "json"]
AudienceType = Literal["beginner", "technical","executive","researcher"]