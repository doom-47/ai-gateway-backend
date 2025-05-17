from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import psycopg2
import os

app = FastAPI()

# DB connection config
DB_URL = os.getenv("DATABASE_URL", "dbname=ai_gateway user=postgres password=postgres host=localhost")

def log_usage(user_id: str, model_name: str, input_tokens: int, output_tokens: int):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (user_id, model_name, input_tokens, output_tokens, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()

class RequestPayload(BaseModel):
    user_id: str
    prompt: str
    model_name: str

@app.post("/generate")
async def generate(payload: RequestPayload):
    # Fake model token usage for illustration
    input_tokens = len(payload.prompt.split())
    output_tokens = 50 if payload.model_name == "gpt-4" else 20

    log_usage(payload.user_id, payload.model_name, input_tokens, output_tokens)

    return {
        "response": f"Generated text using {payload.model_name}",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

@app.get("/usage/{user_id}")
def get_usage(user_id: str):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT model_name, SUM(input_tokens), SUM(output_tokens) FROM usage_log WHERE user_id = %s GROUP BY model_name", (user_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return {"usage": [{"model": row[0], "input_tokens": row[1], "output_tokens": row[2]} for row in data]}
