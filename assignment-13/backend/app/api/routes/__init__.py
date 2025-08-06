from fastapi import APIRouter
from app.api.routes import list_routes, task_routes

api_router = APIRouter()
api_router.include_router(list_routes.router)
api_router.include_router(task_routes.router)