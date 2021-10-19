from fastapi import APIRouter, Depends, FastAPI
from typing import List
from sqlalchemy.orm import Session

from use_case.endpoints_logic import process_get, process_create_item
from model import tracker_model
from model.tracker_model import Expense
from database import database, db_queries

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/expenses/new_expense")
async def create_item(expense: Expense, db: Session = Depends(get_db)):
    return process_create_item(expense, db)


@router.get("/expenses_tracker/{expense_id}")
async def get_expense_id(expense_id, db: Session = Depends(get_db)):
    return process_get(expense_id, db)


@router.get("/expenses/all", response_model=List[tracker_model.Expense])
async def get_expenses(db: Session = Depends(get_db)):
    expenses = list(map(lambda expense: tracker_model.Expense(name=expense.name,
                                                              expenditure=expense.expenditure,
                                                              date=expense.date,
                                                              category=expense.category,
                                                              description=expense.description,
                                                              expense_id=expense.expense_id),
                        db_queries.get_expenses(db, skip=0, limit=100)))
    return expenses
