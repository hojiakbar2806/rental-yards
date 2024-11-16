from sqlalchemy.future import select
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from utils.hashing import hash_password
from core.dependency import get_auth_user
from database.session import get_async_session
from api.auth.schemas import UserOut, UserIn, Token
from core.security import create_access_token, create_refresh_token
from api.auth.dependency import ensure_username, get_validated_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(session: AsyncSession = Depends(get_async_session), user: UserIn = Depends(ensure_username)):
    user.hashed_password = hash_password(user.hashed_password)
    new_user = User(**user.dict())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserOut = Depends(get_validated_user)):
    acces_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return Token(access_token=acces_token, refresh_token=refresh_token)


@router.get("/me")
async def get_me(user: User = Depends(get_auth_user)):
    return user


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def read_all_users(session: AsyncSession = Depends(get_async_session)):
    smt = select(User)
    result = await session.execute(smt)
    users = result.scalars().all()
    return users
