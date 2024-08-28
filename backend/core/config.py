import os
from pathlib import Path
from pydantic_settings import BaseSettings

APP_ENV = os.getenv("ENV", "development")

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
CORE = Path(__file__).resolve().parent

if APP_ENV == "production":
    ENV_FILE = "app" / ".env"
else:
    ENV_FILE = PROJECT_DIR / ".env"

print(ENV_FILE)
print(APP_ENV)


class DBSettings(BaseSettings):
    POSTGRES_DB: str 
    POSTGRES_HOST: str
    POSTGRES_PORT: int 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str

    sql_db_url: str

    @property
    def db_url(self) -> str:
        if APP_ENV == "production":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:
            return f"sqlite+aiosqlite:///{str(BASE_DIR/self.sql_db_url)}"

    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"


class REDISSettings(BaseSettings):
    redis_host: str
    redis_port: int

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"
    
    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"


class JWTSettings(BaseSettings):
    algorithm: str = "RS256"
    private_key_path: Path = CORE / "certs" / "jwt-private.pem"
    public_key_path: Path = CORE / "certs" / "jwt-public.pem"
    access_token_expires_minutes: int = 30
    refresh_token_expires_minutes: int = 60

    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"


class Settings(DBSettings):
    debug: bool = False

    db: DBSettings = DBSettings()
    jwt: JWTSettings = JWTSettings()

    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
