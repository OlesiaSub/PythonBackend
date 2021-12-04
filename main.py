from fastapi import FastAPI

from database import db_models, database
from endpoints.endpoints import router


db_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router)
