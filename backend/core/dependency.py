from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.user import User
from database.session import get_async_session

http_bearer = HTTPBearer()


async def get_auth_user(
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    from models.user import User
    from core.security import verify_user
    return await verify_user(token, session)
