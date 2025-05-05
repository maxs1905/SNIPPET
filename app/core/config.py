from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:project_42@localhost:5432/snippet_dbb"
    SECRET_KEY: str = "NB19Sy3VG0GSm27Q2PjJ3gG693TBpDyQeX_N48866dg"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()