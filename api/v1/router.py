from fastapi import APIRouter
from .controllers import auth_controller, categories_controller, transaction_controller


api_router = APIRouter()
api_router.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
api_router.include_router(categories_controller.router, prefix="/categories")
api_router.include_router(transaction_controller.router, prefix="/transactions")