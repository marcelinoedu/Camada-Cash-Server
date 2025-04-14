from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TransactionCategory(BaseModel):
    id: Optional[UUID] = None
    transaction_id: UUID
    category_id: UUID
    created_at: Optional[datetime] = None
