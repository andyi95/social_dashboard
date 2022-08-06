from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f'{settings.API_STR}/openapi.json'
)