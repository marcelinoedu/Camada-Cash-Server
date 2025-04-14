from typing import List, Optional, Tuple
from models.transaction import Transaction
from repositories.transaction_repository import (
    create_transaction_repository,
    get_transaction_by_id_repository,
    get_all_transactions_repository,
    update_transaction_repository,
    delete_transaction_repository,
)
from datetime import datetime





def create_transaction_service(data: dict) -> Transaction:
    data_dict = data.dict(exclude_unset=True)
    if isinstance(data_dict.get("date"), datetime):
        data_dict["date"] = data_dict["date"].replace(tzinfo=None).isoformat()
    return create_transaction_repository(data_dict)

def get_transaction_by_id_service(transaction_id: str) -> Optional[Transaction]:
    return get_transaction_by_id_repository(transaction_id)


def get_all_transactions_service(
    page: int, limit: int, transaction_type: Optional[str] = None, category_ids: Optional[List[int]] = None
) -> Tuple[List[Transaction], int]:
    return get_all_transactions_repository(page, limit, transaction_type, category_ids)


def update_transaction_service(transaction_id: str, data: dict) -> Optional[Transaction]:
    return update_transaction_repository(transaction_id, data)

def delete_transaction_service(transaction_id: str) -> Optional[Transaction]:
    return delete_transaction_repository(transaction_id)
