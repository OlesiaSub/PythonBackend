from fastapi import FastAPI
from graphene import String, ObjectType, List, Schema, Field
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp

from database import db_models, database
from endpoints.endpoints import router


db_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router)


class ExpenditureInfoType(ObjectType):
    expenditure = String(required=True)
    month = String()


class ExpenseType(ObjectType):
    expense_id = String(required=True)
    name = String(required=True)
    category = String()
    description = String()
    expenditure_info = Field(ExpenditureInfoType)


class Query(ObjectType):
    get_expenses = List(ExpenseType)

    async def resolve_get_expenses(self, info):
        return mock_json


app.add_route("/", GraphQLApp(
    schema=Schema(query=Query),
    executor_class=AsyncioExecutor)
              )

mock_json = [
    {
        "expense_id": "1",
        "name": "First",
        "category": "HW1",
        "description": "first expense",
        "expenditure_info": {
            "expenditure": 100,
            "month": "April"
        }
    },
    {
        "expense_id": "2",
        "name": "Second",
        "category": "HW2",
        "description": "second expense",
        "expenditure_info": {
            "expenditure": 200,
            "month": "March"
        }
    },
    {
        "expense_id": "3",
        "name": "Third",
        "category": "HW3",
        "description": "third expense",
        "expenditure_info": {
            "expenditure": 300,
            "month": "June"
        }
    },
    {
        "expense_id": "4",
        "name": "Fourth",
        "category": "HW4",
        "description": "fourth expense",
        "expenditure_info": {
            "expenditure": 400,
            "month": "January"
        }
    },
]
