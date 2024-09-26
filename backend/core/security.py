import jwt
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials

from core.config import settings
from datetime import datetime, timedelta
from models import User  # Ensure you have the correct import for your User model

PRIVATE_KEY = settings.jwt.private_key_path.read_text()
PUBLIC_KEY = settings.jwt.public_key_path.read_text()
JWT_ALGORITHM = settings.jwt.algorithm

ACCESS_EXP_MIN = settings.jwt.access_token_expires_minutes
REFRESH_EXP_MIN = settings.jwt.refresh_token_expires_minutes


def encode_jwt(payload: dict, token_type: str, expires_delta: timedelta) -> str:
    """
    JWT token yaratish funktsiyasi
    """
    try:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if not isinstance(expires_delta, timedelta):
            raise ValueError("expires_delta must be a timedelta instance")
        exp = now + expires_delta
        to_encode.update({"exp": exp, "iat": now, "type": token_type})
        return jwt.encode(to_encode, PRIVATE_KEY, algorithm=JWT_ALGORITHM)
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token yaratishda xatolik: {str(e)}",
        )


def decode_jwt(token: str) -> dict:
    """
    Tokenni dekodlash
    """
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token eski")
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401, detail=f"Yaroqsiz token: {str(e)}")


def create_access_token(id: int, expires_delta: timedelta | None = None) -> str:
    jwt_payload = {"sub": str(id)}
    expires_delta = expires_delta or timedelta(minutes=ACCESS_EXP_MIN)
    return encode_jwt(jwt_payload, "access", expires_delta)


def create_refresh_token(id: int, expires_delta: timedelta | None = None) -> str:
    jwt_payload = {"sub": str(id)}
    expires_delta = expires_delta or timedelta(minutes=REFRESH_EXP_MIN)
    return encode_jwt(jwt_payload, "refresh", expires_delta)


async def verify_user(token: HTTPAuthorizationCredentials,session: AsyncSession) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentifikatsiya ma'lumotlari yaroqsiz",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt(token.credentials)
        user_id = payload.get("sub")
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    return user
