from pydantic import BaseModel
from datetime import datetime

class UsageLog(BaseModel):
    id: int
    user_id: str
    model_name: str
    input_tokens: int
    output_tokens: int
    timestamp: datetime
