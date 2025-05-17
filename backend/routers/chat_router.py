from fastapi import APIRouter
from pydantic import BaseModel
from backend.db.database import get_connection
from backend.services.openai_service import generate_text

router = APIRouter()

class RequestPayload(BaseModel):
    user_id: str
    prompt: str
    model_name: str

def log_usage(user_id: str, model_name: str, input_tokens: int, output_tokens: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
        """,
        (user_id, model_name, input_tokens, output_tokens)
    )
    conn.commit()
    cursor.close()
    conn.close()

@router.post("/generate")
async def generate(payload: RequestPayload):
    input_tokens = len(payload.prompt.split())
    # For example, output tokens depends on model (simplified)
    output_tokens = 50 if payload.model_name == "gpt-4" else 20

    response = generate_text(payload.prompt, payload.model_name)
    log_usage(payload.user_id, payload.model_name, input_tokens, output_tokens)

    return {
        "response": response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

@router.get("/usage/{user_id}")
def get_usage(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT model_name, SUM(input_tokens), SUM(output_tokens) 
        FROM usage_log WHERE user_id = %s GROUP BY model_name
        """,
        (user_id,)
    )
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {
        "usage": [
            {"model": row[0], "input_tokens": row[1], "output_tokens": row[2]}
            for row in data
        ]
    }
