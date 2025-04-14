from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[UUID] = None
    amount: float
    type: Literal["income", "outcome"]
    status: bool
    description: Optional[str] = None
    date: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
