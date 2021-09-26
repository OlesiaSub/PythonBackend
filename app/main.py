from fastapi import FastAPI

from model.tracker_model import Expense
from endpoints.endpoints import router

app = FastAPI()

app.include_router(router)