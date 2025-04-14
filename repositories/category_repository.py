from db.supabase import get_supabase
from models.category import Category
from postgrest.exceptions import APIError
from typing import List

def fetch_categories_by_type(category_type: str) -> List[Category]:
    supabase = get_supabase()

    try:
        result = (
            supabase.table("categories")
            .select("*")
            .eq("type", category_type)
            .execute()
        )

        if result.data:
            return [Category(**item) for item in result.data]

    except APIError as e:
        print(f"[fetch_categories_by_type] Erro: {e.message}")

    return []


def fetch_categories() -> List[Category]:
    supabase = get_supabase()

    try:
        result = (
            supabase.table("categories")
            .select("*")
            .execute()
        )
        if result.data:
            return [Category(**item) for item in result.data]

    except APIError as e:
        print(f"[fetch_categories_by_type] Erro: {e.message}")

    return []
