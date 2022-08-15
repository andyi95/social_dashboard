from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import main_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost/',
    'http://127.0.0.1:4000/',
    'http://localhost:4000/'
]
app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(main_router, prefix=settings.API_STR)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in origins],
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)