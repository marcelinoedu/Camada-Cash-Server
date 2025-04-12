from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    id: str
    user_id: str
    token: str
    token_type: str
    active: bool
    created_at: datetime
    updated_at: datetime
    expires_at: datetime

        
        