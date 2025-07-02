from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"

    @property
    def DATABASE_URL(self):
        dsn = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return dsn


settings = Settings()  # type: ignore
