import random
import string
from hashlib import sha256
import bcrypt
from utils.sanitize import sanitize_user
from repositories.user_repository import get_all_users, update_user, delete_user, update_user, delete_user, get_user_by_id as get_user_by_id_repo
from models.user import User



def generate_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_users():
    users = get_all_users()
    if not users:
        return None
    return users


def get_user_by_id(user_id: str) -> User | None:
    if not user_id:
        raise ValueError("O ID do usuário é obrigatório.")
    user = get_user_by_id_repo(user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")
    return sanitize_user(user)


def update_user_service(user_id: str, name: str, email: str, role: str,  status: str) -> User | None:
    if not all([user_id, name, email, role, status]):
        raise ValueError("Todos os campos são obrigatórios.")

    return update_user(user_id, name, email, role, status)


def delete_user_service(user_id: str) -> User | None:
    if not user_id:
        raise ValueError("O ID do usuário é obrigatório.")

    return delete_user(user_id)
