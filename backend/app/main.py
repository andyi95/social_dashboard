from fastapi import FastAPI, APIRouter, Path, Depends, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routers import main_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from app.core.init_app import register_db
from app.schemas import WordStats, UserAuth


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
register_db(app)


@AuthJWT.load_config
def get_config():
    return settings

@app.exception_handler(AuthJWTException)
def auth_exc_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )

