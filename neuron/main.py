import sqlite3

from server.constants import products_sqlite, products_table
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from server.sanity import log_db_status, test_valkey
from server.search import flush_user_memory, run_for_user, user_exists

app = FastAPI()
log_db_status()
test_valkey()


# Allow frontend on localhost:3000 or wherever you're hosting React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserQuery(BaseModel):
    user_id: str
    user_input: str


@app.post("/query")
def handle_query(data: UserQuery):
    neuron_out = run_for_user(data.user_id, data.user_input)
    sql_query = neuron_out["sql_query"]
    justification = neuron_out["justification"]
    follow_up = neuron_out["follow_up"]

    conn = sqlite3.connect(products_sqlite)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dicts
    products = [dict(row) for row in rows]
    res = {"products": products, "justification": justification, "follow_up": follow_up}
    print(res)
    return res


@app.get("/products")
def fetch_all_products():
    conn = sqlite3.connect(products_sqlite)
    conn.row_factory = sqlite3.Row  # to get dict-like rows
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {products_table}")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dicts
    products = [dict(row) for row in rows]
    print(products)
    return {"products": products}


@app.post("/flush")
def flush_memory(user_id: str = Query(..., description="User ID to flush memory for")):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User ID not found")
    flush_user_memory(user_id)
    return {"message": f"Memory flushed for user_id: {user_id}"}
