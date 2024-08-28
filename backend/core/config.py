import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
CORE = Path(__file__).resolve().parent

class GlobalSettings(BaseSettings):
    debug: bool = True
    app_env: str = "development"

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

global_settings = GlobalSettings()


class DBSettings(BaseSettings):
    POSTGRES_DB: str 
    POSTGRES_HOST: str
    POSTGRES_PORT: int 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    sql_db_url: str

    @property
    def url(self) -> str:
        if global_settings.app_env == "production":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:
            return f"sqlite+aiosqlite:///{str(BASE_DIR/self.sql_db_url)}"

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

class REDISSettings(BaseSettings):
    redis_host: str
    redis_port: int

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"
    
    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

# JWTSettings klassi
class JWTSettings(BaseSettings):
    algorithm: str = "RS256"
    private_key_path: Path = CORE / "certs" / "jwt-private.pem"
    public_key_path: Path = CORE / "certs" / "jwt-public.pem"
    access_token_expires_minutes: int = 30
    refresh_token_expires_minutes: int = 60

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

class Settings(DBSettings):
    debug: bool = global_settings.debug

    db: DBSettings = DBSettings()
    jwt: JWTSettings = JWTSettings()

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

print("---------------------")
print(global_settings.app_env)
print("---------------------")
print(global_settings.debug)
print("---------------------")
print(settings.db.url)
print("---------------------")
