from models.user import User
from models.token import Token

def sanitize_user(user: User):
    return user.dict(exclude={"password"})


def sanitize_token(token: Token):
    return {
        "token": token.token,
        "token_type": token.token_type,
        "expires_at": token.expires_at.isoformat(),
        "created_at": token.created_at.isoformat(),
    }