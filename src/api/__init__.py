from fastapi import APIRouter

from src.api import jokes

endpoints = APIRouter()
endpoints.include_router(jokes.router)

