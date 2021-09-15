from fastapi import FastAPI

from app.model import Expense

app = FastAPI()


@app.get("/expenses_tracker/{expense_id}")
async def get_expense_id(expense_id):
    return {"expense_id": expense_id}


@app.post("/expenses/")
async def create_item(expense: Expense):
    return expense
