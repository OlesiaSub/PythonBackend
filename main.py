from fastapi import FastAPI

from endpoints.endpoints import router

app = FastAPI()

app.include_router(router)
