from models.token import Token
from db.supabase import get_supabase
from postgrest.exceptions import APIError


def get_token(token: str) -> Token | None:
    supabase = get_supabase()
    try:
        result = supabase.table("tokens").select("*").eq("token", token).execute()
        if result.data:
            return Token(**result.data[0])
    except APIError as e:
        print(f"[get_token] Erro: {e.message}")
    return None


def get_token_by_user_id(user_id: str, token_type: str) -> Token | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("tokens")
            .select("*")
            .eq("user_id", user_id)
            .eq("token_type", token_type)
            .execute()
        )
        if result.data:
            return Token(**result.data[0])
    except APIError as e:
        print(f"[get_token_by_user_id] Erro: {e.message}")
    return None


def insert_token(user_id: str, token: str, token_type: str, expires_at: str) -> Token | None:
    supabase = get_supabase()
    try:
        result = supabase.table("tokens").insert({
            "user_id": user_id,
            "token": token,
            "token_type": token_type,
            "expires_at": expires_at
        }).execute()
        if result.data:
            return Token(**result.data[0])
    except APIError as e:
        print(f"[insert_token] Erro: {e.message}")
        print("Detalhes:", e.details)
        print("Dica:", e.hint)
    return None


def revoque_token(token: str) -> Token | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("tokens")
            .update({"active": False})
            .eq("token", token)
            .execute()
        )
        if result.data:
            return Token(**result.data[0])
    except APIError as e:
        print(f"[revoque_token] Erro: {e.message}")
    return None


def revove_all_tokens_by_user_id(user_id: str, token_type: str) -> Token | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("tokens")
            .update({"active": False})
            .eq("user_id", user_id)
            .eq("token_type", token_type)
            .execute()
        )
        if result.data:
            return Token(**result.data[0])
    except APIError as e:
        print(f"[revove_all_tokens_by_user_id] Erro: {e.message}")
    return None
