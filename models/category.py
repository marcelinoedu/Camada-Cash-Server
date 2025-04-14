from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class Category(BaseModel):
    id: Optional[UUID]
    label: str
    category_type: str = Field(..., alias="type") 
