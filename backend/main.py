from urllib.parse import unquote

from api.v1.router import v1_router
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from database.session import create_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

MEDIA_DIR = "media"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="FastAPI",
    description="FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "It works"}


@app.get("/media/{path:path}")
async def read_media(path: str):
    file_path = unquote(f"{MEDIA_DIR}/{path}")
    return FileResponse(file_path)