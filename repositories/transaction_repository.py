from db.supabase import get_supabase
from models.transaction import Transaction
from postgrest.exceptions import APIError
from typing import List, Optional, Tuple


def link_transaction_to_category(transaction_id: str, category_id: str) -> bool:
    supabase = get_supabase()
    try:
        result = supabase.table("transaction_categories").insert({
            "transaction_id": str(transaction_id),
            "category_id": str(category_id)
        }).execute()

        return bool(result.data)
    except APIError as e:
        print(f"[link_transaction_to_category] Erro: {e.message}")
        return False


def create_transaction_repository(data: dict) -> Optional[Transaction]:
    supabase = get_supabase()
    try:
    
        print(f"[create_transaction] data: {data}")
        result = supabase.table("transactions").insert(data).execute()
        print(f"[create_transaction] result: {result}")
        if result.data:
            return Transaction(**result.data[0])
    except APIError as e:
        print(f"[create_transaction] Erro: {e.message}")
    return None

def get_transaction_by_id_repository(transaction_id: str) -> Optional[Transaction]:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("transactions")
            .select("*")
            .eq("id", str(transaction_id))
            .execute()
        )
        if result.data:
            return Transaction(**result.data[0])
    except APIError as e:
        print(f"[get_transaction_by_id] Erro: {e.message}")
    return None

def get_all_transactions_repository(
    page: int,
    limit: int,
    transaction_type: Optional[str] = None,
    category_ids: Optional[List[str]] = None,
) -> Tuple[List[Transaction], int]:
    supabase = get_supabase()
    from_index = (page - 1) * limit
    to_index = from_index + limit - 1


    query = supabase.table("transactions").select("*", count="exact")
    if transaction_type:
        query = query.eq("type", transaction_type)

    

    if category_ids:
        transaction_ids_result = (
            supabase.table("transaction_categories")
            .select("transaction_id")
            .in_("category_id", category_ids)
            .execute()
        )

        if transaction_ids_result.error:
            print("[Supabase Category Filter Error]", transaction_ids_result.error.message)
            return [], 0

        filtered_ids = list({row["transaction_id"] for row in (transaction_ids_result.data or [])})

        if not filtered_ids:
            return [], 0 

        query = query.in_("id", filtered_ids)

    query = query.range(from_index, to_index).order("date", desc=True)

    result = query.execute()
    
    transactions = [Transaction(**t) for t in result.data] if result.data else []
    if not transactions:
        return [], 0
    
    total = result.count or 0

    return transactions, total



def update_transaction_repository(transaction_id: str, data: dict) -> Optional[Transaction]:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("transactions")
            .update(data)
            .eq("id", str(transaction_id))
            .execute()
        )
        if result.data:
            return Transaction(**result.data[0])
    except APIError as e:
        print(f"[update_transaction] Erro: {e.message}")
    return None

def delete_transaction_repository(transaction_id: str) -> Optional[Transaction]:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("transactions")
            .delete()
            .eq("id", str(transaction_id))
            .execute()
        )
        if result.data:
            return Transaction(**result.data[0])
    except APIError as e:
        print(f"[delete_transaction] Erro: {e.message}")
    return None


