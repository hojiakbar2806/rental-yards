from .auth import auth_router
from fastapi import APIRouter

v1_router = APIRouter()


v1_router.include_router(auth_router)
