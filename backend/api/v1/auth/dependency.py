from fastapi import Depends
from api.v1.auth import schemas
from fastapi.security import HTTPBearer
from api.v1.auth import utils as auth_utils
from database.session import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

http_bearer = HTTPBearer()


async def ensure_username(user: schemas.UserIn, session: AsyncSession = Depends(get_async_session)) -> schemas.UserIn:
    return await auth_utils.exist_username(user, session)


async def get_validated_user(user: schemas.Login, session: AsyncSession = Depends(get_async_session)):
    return await auth_utils.validate_get_user(user.username, user.password, session)
