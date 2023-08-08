from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator
import secrets
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str = os.getenv('DB_HOST', 'db')
    POSTGRES_USER: str = os.getenv('DB_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    POSTGRES_DB: str = os.getenv('DB_NAME', 'dashboard-tortoise')
    PROJECT_NAME: str = 'Social Dashboard'
    API_STR: str = '/api'
    APPLICATIONS = [
        'app'
    ]
    DB_URL = f'postgres://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:5432/{os.getenv("DB_NAME")}'
    DB_CONNECTIONS = {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'db_url': DB_URL,
                'credentials': {
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'port': '5432',
                    'user': os.getenv('DB_USER', 'postgres'),
                    'password': os.getenv('DB_PASSWORD', 'postgres'),
                    'database': os.getenv('DB_NAME', 'dashboard-tortoise'),
                }
            },
        }


    authjwt_secret_key = SECRET_KEY


settings = Settings()
DB_URL = f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:5432/{settings.POSTGRES_DB}'
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


