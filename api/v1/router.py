from fastapi import APIRouter
from .controllers import auth_controller


api_router = APIRouter()
api_router.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])