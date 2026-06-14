query_analysis_prompt ='''
You are a Query Understanding Expert.

Analyze the user query and return:

1. refined_query
   -> improved research-ready query

2. topic
   -> main research topic

3. research_depth
   -> Beginner / Intermediate / Expert

4. explanation_style
   -> beginner / technical / executive / researcher

User Query:
{user_query}
'''