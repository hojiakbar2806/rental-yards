from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database.base import Base

async_engine = create_async_engine(settings.url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession: 
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    """Create database tables if they do not exist."""
    async with async_engine.begin() as conn:
        # Creates tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    print("Ma'lumotlar ombori tiklandi")
