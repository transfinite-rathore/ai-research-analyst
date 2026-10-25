import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

def sql_checkpointer():
    # 1. Setup paths
    DB_DIR = Path("db/data")
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DB_DIR / "ai_analyst_cp.sqlite"

    # 2. Open the connection ONCE (check_same_thread=False is important for FastAPI)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    # 3. Create the checkpointer ONCE
    checkpointer = SqliteSaver(conn)
    return checkpointer