from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from core.config import settings
from models.user import User
from repositories.token_repository import get_token_by_user_id, insert_token, revove_all_tokens_by_user_id, revoque_token as repo_revoke_token
from models.token import Token
import random
import string


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 60 * 24 * 7

RECOVER_PASSWORD_EXPIRES_MINUTES = 5


def generate_user_token(user: User, token_type: str) -> Token:
    user_token = get_token_by_user_id(user.id, token_type) if token_type == "Bearer" else None

    if user_token and user_token.active:
        if isinstance(user_token.expires_at, str):
            user_token.expires_at = datetime.fromisoformat(
                user_token.expires_at)

        if user_token.expires_at > datetime.now(timezone.utc):
            return user_token

    revove_all_tokens_by_user_id(user_id=user.id, token_type=token_type)

    new_token = generate_jwt_token(
        user) if token_type == "Bearer" else generate_recover_password_token()

    return insert_token(user_id=user.id, token=new_token["token"], token_type=token_type, expires_at=new_token["expires_at"])

def generate_recover_password_token() -> dict:
    expire = datetime.utcnow() + timedelta(minutes=RECOVER_PASSWORD_EXPIRES_MINUTES)

    token = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    return {
        "token": token,
        "expires_at": expire.isoformat()
    }


def generate_jwt_token(user: User) -> dict:
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MINUTES)

    payload = {
        "sub": user.id,
        "email": user.email,
        "exp": expire
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "token": token,
        "expires_at": expire.isoformat()
    }


def verify_token(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def revoke_token(token: str) -> Token:
    return repo_revoke_token(token=token)
