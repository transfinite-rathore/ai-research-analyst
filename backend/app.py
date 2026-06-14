from fastapi import FastAPI
import uuid
from ..workflow.workflow import workflow

app=FastAPI()

@app.get("/")
def home():
    return {"message":"You are home"}

@app.post("/user_query/{user_query}")
def research_topic(user_query:str):
    initial_state = {
    "query": {
        "user_query": user_query
    },
    "research_iteration": 0
}
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }
    
    response=workflow.invoke(initial_state,config=config)
    return {"workflow_response":response}