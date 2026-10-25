from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from langgraph.types import Command
from .models.resume_query import ResumeRequest
from .models.user_query import UserQuery
from config.chechpointer_config import sql_checkpointer
from state_saver.json_saver import JSONSaver
from workflow.workflow import AnalystWorkflow
from config.latency_tracker import track_time
import logging

logger=logging.getLogger(__name__)




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


checkpointer=sql_checkpointer()
workflow=AnalystWorkflow(checkpointer)


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

@track_time
@app.post("/data")
def data(data: UserQuery):
    try:
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id,"research_mode": "parallel"}}
        # initial_state = {
        #     "query": {"user_query": data.user_query},
        #     "research_iteration": 0,
        # }
        
        result = workflow.run(data.user_query, config=config)
        response=to_response(thread_id, result)
        file_name= ""
        if response["status"]=="complete":
            file_name=f"{thread_id}_complete.json"
        else:
            file_name=f"{thread_id}_interrupt.json"
        JSONSaver().save(filename=file_name,data=result)
        return response

    except Exception:
        logger.exception("Workflow execution failed")
        raise HTTPException(status_code=500, detail="Research workflow failed.")


@track_time
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
        response=to_response(thread_id, result)
        if response["status"]=="complete":
            JSONSaver().save(filename=f"{thread_id}_resume_complete.json",data=result)
        return response

    except HTTPException:
        raise
    except Exception:
        logger.exception("Resume failed")
        raise HTTPException(status_code=500, detail="Resume failed.")

