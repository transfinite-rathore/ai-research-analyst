from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
from pathlib import Path
from workflow.workflow import workflow
import logging

logger=logging.getLogger(__name__)


# from ..workflow.workflow import workflow

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

@app.get("/")
def home():
    return {"message": "You are home"}



@app.post("/data")
def data(data: UserQuery):

    try:
        initial_state = {
            "query": {
                "user_query": data.user_query
            },
            "research_iteration": 0
        }

        config = {
            "configurable": {
                "thread_id": str(uuid.uuid4())
            }
        }

        response = workflow.invoke(initial_state, config=config)

        base_dir = Path(__file__).resolve().parent.parent

        state_dir = base_dir/"db" / "state_data"
        state_dir.mkdir(parents=True, exist_ok=True)

        state_file = state_dir / "final_state.json"

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(
                response,
                f,
                indent=4,
                default=str
            )

        return {
            "response": response["final_report"]
        }

    except Exception:
        logger.exception("Workflow execution failed")

        raise HTTPException(
            status_code=500,
            detail="Research workflow failed."
        )

# @app.post("/data")
# def data(data:UserQuery):
#     print(data.user_query)
#     # return {"response":"kalme gand marra"}
#     try:
#         initial_state = {
#             "query": {
#                 "user_query": data.user_query
#             },
#             "research_iteration": 0
#         }
#         config = {
#             "configurable": {
#                 "thread_id": str(uuid.uuid4())
#             }
#         }
#         response = workflow.invoke(initial_state, config=config)
#         file = Path(__file__).resolve().parent
#         state_data=file/"state_data"/"final_state,json"
        
#         with open(state_data, "w", encoding="utf-8") as f:
#             json.dump(
#                 response,
#                 f,
#                 indent=4,
#                 default=str
#             )
#         return {"response": response["final_report"]}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e))

# @app.post("/user_query/{user_query}")
# def research_topic(user_query: str):
#     initial_state = {
#         "query": {
#             "user_query": user_query
#         },
#         "research_iteration": 0
#     }

#     config = {
#         "configurable": {
#             "thread_id": str(uuid.uuid4())
#         }
#     }

#     response = workflow.invoke(initial_state, config=config)
#     return {"workflow_response": response}