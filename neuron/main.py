import sqlite3

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .intelligence.flow import SearchFlow
from .server import products_sqlite, products_table, log_db_status
from .memory import test_valkey, ConversationStore, AxesStore
from .intelligence.axes import Axes


app = FastAPI()
log_db_status()
test_valkey()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserQuery(BaseModel):
    user_id: str
    user_input: str


@app.post("/query")
def handle_query(data: UserQuery):
    conv_store = ConversationStore(data.user_id)
    conv_store.save({"role": "user", "content": data.user_input})

    axes_store = AxesStore(data.user_id)

    flow = SearchFlow()
    result = flow.kickoff(
        inputs={
            "conversation": conv_store.get_all(),
            "search_space": axes_store.latest() if axes_store.latest() is not None else Axes(),
        }
    )
    justification = result["justification"]
    followup = result["followup"]
    products = result["skus"]
    search_space = result["search_space"]

    conv_store.save({"role": "assistant", "content": f"<justification>{justification}</justification>{followup}"})
    axes_store.save(search_space)

    return {"products": products, "justification": justification, "follow_up": followup}


@app.get("/conversation/{user_id}")
def get_conversation(user_id: str):
    conv_store = ConversationStore(user_id)
    return {"conversation": conv_store.get_all()}


@app.get("/products")
def fetch_all_products():
    conn = sqlite3.connect(products_sqlite)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {products_table}")
    rows = cursor.fetchall()
    conn.close()

    products = [dict(row) for row in rows]
    return {"products": products}


@app.post("/flush")
def flush_memory(user_id: str = Query(..., description="User ID to flush memory for")):
    conv_store = ConversationStore(user_id)
    conv_already_empty = not conv_store.get_all()
    conv_store.flush()

    axes_store = AxesStore(user_id)
    axes_already_empty = not axes_store.latest() is None
    axes_store.flush()

    message = f"Memory flushed for user_id: {user_id}. "
    if conv_already_empty:
        message += "Conversations were already empty. "
    if axes_already_empty:
        message += "Search space was already None."

    return {"message": message}
