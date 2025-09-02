# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    SQLALCHEMY_DATABASE_URI: str = ""
    DB_SCHEMA: str = "public"

    class Config:
        env_file = ".env"

    def get_database_uri(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
settings.SQLALCHEMY_DATABASE_URI = settings.get_database_uri()
