from tortoise import Tortoise
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings

def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={'models': ['models']},
        generate_schemas=False,
        add_exception_handlers=True
    )

def get_app_list():
    app_list = [f'{app}.models' for app in settings.APPLICATIONS]
    return app_list

def register_db(app: FastAPI, db_url: str = None):
    db_url = db_url or settings.DB_URL
    app_list = get_app_list()
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': app_list},
        generate_schemas=True,
        add_exception_handlers=True,
    )
Tortoise.init_models(get_app_list(), 'models')