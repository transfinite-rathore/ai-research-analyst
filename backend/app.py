from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
from pathlib import Path
from workflow.workflow import AnalystWorkflow
import logging

logger=logging.getLogger(__name__)


workflow=AnalystWorkflow()

app = FastAPI()

# CORS Configuration
origins = [
   "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow all headers
)

class UserQuery(BaseModel):
    user_query:str

def to_response(thread_id: str, result: dict) -> dict:
    interrupts = result.get("__interrupt__")
    if interrupts:
        return {
            "thread_id": thread_id,
            "status": "waiting_for_approval",
            "payload": interrupts[0].value,
        }
    return {
        "thread_id": thread_id,
        "status": "complete",
        "response": result.get("final_report"),
    }
    
@app.get("/")
def home():
    return {"message": "You are home"}

@app.post("/data")
def data(data: UserQuery):
    try:
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        # initial_state = {
        #     "query": {"user_query": data.user_query},
        #     "research_iteration": 0,
        # }

        result = workflow.run(data.user_query, config=config)
        return to_response(thread_id, result)

    except Exception:
        logger.exception("Workflow execution failed")
        raise HTTPException(status_code=500, detail="Research workflow failed.")

class ResumeRequest(BaseModel):
    answer: str
    feedback: str | None = None
    edited_insights: dict | None = None


@app.post("/data/{thread_id}/resume")
def resume(thread_id: str, body: ResumeRequest):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = workflow.graph.get_state(config)
        if not state.values:
            raise HTTPException(status_code=404, detail="Unknown thread_id.")
        if AnalystWorkflow.APPROVER not in state.next:
            raise HTTPException(status_code=409, detail="Run is not waiting for approval.")

        answer = body.model_dump(exclude_none=True)
        result = workflow.graph.invoke(Command(resume=answer), config=config)
        return to_response(thread_id, result)

    except HTTPException:
        raise
    except Exception:
        logger.exception("Resume failed")
        raise HTTPException(status_code=500, detail="Resume failed.")


# @app.post("/data")
# def data(data: UserQuery):

#     try:
#         initial_state = {
#             "query": {
#                 "user_query": data.user_query
#             },
#             "research_iteration": 0
#         }
#         thread_id=str(uuid.uuid4())
#         config = {
#             "configurable": {
#                 "thread_id": thread_id
#             }
#         }

#         response = workflow.invoke(initial_state, config=config)

#         base_dir = Path(__file__).resolve().parent.parent

#         state_dir = base_dir/"db" / "state_data"
#         state_dir.mkdir(parents=True, exist_ok=True)

#         state_file = state_dir / "final_state_101.json"

#         with open(state_file, "w", encoding="utf-8") as f:
#             json.dump(
#                 response,
#                 f,
#                 indent=4,
#                 default=str
#             )
#         return { "response": response["final_report"] }

#         # return {
#         #     "thread_id":thread_id,
#         #     "status":"Complete",
#         #     "response": response["final_report"]
#         # }

#     except Exception:
#         logger.exception("Workflow execution failed")

#         raise HTTPException(
#             status_code=500,
#             detail="Research workflow failed."
#         )

# @app.post("/research/{thread_id}/resume")
# def resume(thread_id:str):
#     config={
#         "configurable":{
#             "thread_id":thread_id
#         }
#     }
#     snapshot = workflow.get_state(config)

#     if snapshot is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Thread not found."
#         )

#     result = workflow.invoke(
#         None,
#         config=config
#     )

#     # return result
#     return {
#             "thread_id":thread_id,
#             "status":"Complete",
#             "response": result["final_report"]
#         }