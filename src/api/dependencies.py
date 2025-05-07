from fastapi import APIRouter

from src.api.routes.snippets import user_router
from src.api.routes.auth import auth_router


api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(auth_router)