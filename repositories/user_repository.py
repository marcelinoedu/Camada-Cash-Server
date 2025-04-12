from db.supabase import get_supabase
from models.user import User
from postgrest.exceptions import APIError
from utils.sanitize import sanitize_user



def get_user_by_email(email: str) -> User | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )
        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[get_user_by_email] Erro: {e.message}")
    return None


def get_user_by_id(user_id: str) -> User | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )
        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[get_user_by_id] Erro: {e.message}")
    return None


def insert_user(name: str, email: str, password: str) -> User | None:
    supabase = get_supabase()

    try:
        result = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password,
        }).execute()

        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[insert_user] Erro: {e.message}")
    return None


def update_user(user_id: str, name: str, email: str, role: str, status: str) -> User | None:
    supabase = get_supabase()

    try:
        result = supabase.table("users").update({
            "name": name,
            "email": email,
            "status": status,
            "role": role,
        }).eq("id", user_id).execute()

        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[update_user] Erro: {e.message}")
    return None


def delete_user(user_id: str) -> User | None:
    supabase = get_supabase()

    try:
        result = supabase.table("users").delete().eq("id", user_id).execute()
        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[delete_user] Erro: {e.message}")
    return None


def get_all_users() -> list[User]:
    supabase = get_supabase()
    try:
        result = supabase.table("users").select("*").execute()
        if result.data:
            return [sanitize_user(User(**user)) for user in result.data]
    except APIError as e:
        print(f"[get_all_users] Erro: {e.message}")
    return []

def get_user_by_id(user_id: str) -> User | None:
    supabase = get_supabase()
    try:
        result = (
            supabase.table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )
        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[get_user_by_id] Erro: {e.message}")
    return None


def update_password(user_id: str, password: str):
    supabase = get_supabase()
    try:
        result = supabase.table("users").update({
            "password": password,
        }).eq("id", user_id).execute()

        if result.data:
            return User(**result.data[0])
    except APIError as e:
        print(f"[update_user] Erro: {e.message}")
    return None
    
