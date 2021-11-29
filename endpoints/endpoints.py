from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import database, db_queries
from model import tracker_model
from model.tracker_model import Expense
from use_case.endpoints_logic import process_get_expense_by_id, process_create_expense, process_get_group

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/expenses/new_expense")
async def create_expense(expense: Expense, db: Session = Depends(get_db)):
    return process_create_expense(expense, db)


@router.get("/expenses_tracker/{expense_id}")
async def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    return process_get_expense_by_id(expense_id, db)


@router.get("/expenses/all", response_model=List[tracker_model.Expense])
async def get_expenses_of_user(user_id: int, db: Session = Depends(get_db)):
    expenses = list(map(lambda expense: tracker_model.Expense(name=expense.name,
                                                              expenditure=expense.expenditure,
                                                              date=expense.date,
                                                              category=expense.category,
                                                              description=expense.description,
                                                              expense_id=expense.expense_id,
                                                              user_id=expense.user_id),
                        db_queries.get_user_expenses(db, user_id=user_id, limit=100)))
    return expenses


@router.get("/expenses_tracker/{group_id}")
async def get_group_info(group_id, db: Session = Depends(get_db)):
    return process_get_group(group_id, db)
