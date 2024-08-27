from models.user import User
from api.v1.auth import schemas
from utils import hash_password
from sqlalchemy.future import select
from core.dependency import get_auth_user
from api.v1.auth import dependency as deps
from database.session import get_async_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import create_access_token, create_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
        session: AsyncSession = Depends(get_async_session),
        user: schemas.UserIn = Depends(deps.ensure_username),
):
    user.hashed_password = hash_password(user.hashed_password)
    new_user = User(**user.dict())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: schemas.UserOut = Depends(deps.get_validated_user)):
    acces_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return schemas.Token(
        access_token=acces_token,
        refresh_token=refresh_token,
        type="bearer"
    )


@router.get("/me")
async def get_me(user: User = Depends(get_auth_user)):
    return user


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def read_all_users(session: AsyncSession = Depends(get_async_session)):
    smt = select(User)
    result = await session.execute(smt)
    users = result.scalars().all()
    return users
