from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from services.token_service import verify_token
from repositories.token_repository import get_token
from repositories.user_repository import get_user_by_id

PUBLIC_PATHS = [
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/auth/forgot_password",
    "/api/v1/auth/validate_code",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/"
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "Token não fornecido"})

        token = auth_header.split(" ")[1]
        payload = verify_token(token=token)

        if not payload:
            return JSONResponse(status_code=401, content={"message": "Token inválido ou expirado"})

        token_data = get_token(token=token)
        if not token_data or (not token_data.active):
            return JSONResponse(status_code=401, content={"message": "Token revogado ou inválido"})

        user = get_user_by_id(payload["sub"])
        if not user:
            return JSONResponse(status_code=404, content={"message": "Usuário não encontrado"})

        request.state.user = user

        return await call_next(request)
