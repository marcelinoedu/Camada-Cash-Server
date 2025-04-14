

from pydantic import BaseModel

class TransactionCategoryLinkRequest(BaseModel):
    category_id: str
