from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator
import secrets
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str = os.getenv('DB_HOST', 'db')
    POSTGRES_USER: str = os.getenv('DB_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    POSTGRES_DB: str = os.getenv('DB_NAME', 'postgres')
    PROJECT_NAME: str = 'Social Dashboard'
    API_STR: str = '/api'

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

settings = Settings()
