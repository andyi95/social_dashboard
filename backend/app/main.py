from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import main_router

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(main_router, prefix=settings.API_STR)
