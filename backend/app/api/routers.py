from fastapi import APIRouter
from app.api import views

main_router = APIRouter()
main_router.include_router(views.router, tags=['words'])
