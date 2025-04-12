from fastapi import FastAPI
from api.v1.router import api_router
from core.config import settings
from starlette.middleware import Middleware
from middlewares.auth_middleware import AuthMiddleware

middleware = [
    Middleware(AuthMiddleware)
]

app = FastAPI(title=settings.PROJECT_NAME, middleware=middleware)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
