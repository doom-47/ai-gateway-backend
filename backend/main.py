from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# DB connection config from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ai_gateway")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def log_usage(user_id: str, model_name: str, input_tokens: int, output_tokens: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, model_name, input_tokens, output_tokens, datetime.utcnow()))
        conn.commit()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

class RequestPayload(BaseModel):
    user_id: str
    prompt: str
    model_name: str

@app.post("/generate")
async def generate(payload: RequestPayload):
    # Simple token counting (count words in prompt)
    input_tokens = len(payload.prompt.split())
    # Fake output tokens count, e.g., 50 for gpt-4, else 20
    output_tokens = 50 if payload.model_name == "gpt-4" else 20

    # Log usage to DB
    log_usage(payload.user_id, payload.model_name, input_tokens, output_tokens)

    # Return fake generated text
    return {
        "response": f"Generated text using model {payload.model_name}",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

@app.get("/usage/{user_id}")
async def get_usage(user_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, user_id, model_name, input_tokens, output_tokens, timestamp 
            FROM usage_log 
            WHERE user_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 10
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No usage found for user_id")
        return {"user_id": user_id, "usage": rows}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()
