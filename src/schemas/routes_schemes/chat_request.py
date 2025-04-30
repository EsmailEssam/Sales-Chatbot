from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_query: str
    session_id: Optional[str] = None
