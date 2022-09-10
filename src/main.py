from fastapi import FastAPI

from src import api

app = FastAPI()

app.include_router(api.endpoints)
