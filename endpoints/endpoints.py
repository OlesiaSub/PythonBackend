from array import array
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import database, db_queries
from model import tracker_model
from model.tracker_model import Expense, User, Group
from use_case.endpoints_logic import process_create_expense, process_get_group, \
    process_create_user, process_get_user_expense_by_id, process_create_group

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


@router.post("/expenses/new_user")
async def create_user(user: User, db: Session = Depends(get_db)):
    return process_create_user(user, db)


@router.post("/expenses/new_group")
async def create_group(group: Group, participants_ids: list[int], db: Session = Depends(get_db)):
    return process_create_group(group, participants_ids, db)


@router.get("/user/{user_id}/expenses/{expense_id}")
async def get_expense_by_id(user_id: int, expense_id: int, db: Session = Depends(get_db)):
    return process_get_user_expense_by_id(user_id, expense_id, db)


@router.get("/user/{user_id}/expenses", response_model=List[tracker_model.Expense])
async def get_expenses_of_user(user_id: int, db: Session = Depends(get_db)):
    expenses = list(map(lambda expense: tracker_model.Expense(name=expense.name,
                                                              expenditure=expense.expenditure,
                                                              date=expense.date,
                                                              category=expense.category,
                                                              description=expense.description,
                                                              expense_id=expense.expense_id,
                                                              user_id=expense.user_id,
                                                              group_id=Expense.group_id),
                        db_queries.get_user_expenses(db, user_id=user_id, limit=100)))
    return expenses


@router.get("/groups/{group_id}")
async def get_group_info(group_id, db: Session = Depends(get_db)):
    return process_get_group(group_id, db)


@router.get("/groups/{group_id}/expenses")
async def get_group_expenses(group_id, db: Session = Depends(get_db)):
    return db_queries.get_group_expenses(db, group_id)


@router.get("/groups/{group_id}/{user_id}/expenses")
async def get_group_expenses_of_user(group_id, user_id, db: Session = Depends(get_db)):
    return db_queries.get_group_expenses_of_user(db, group_id, user_id)


@router.get("/user/{user_id}}/groups")
async def get_groups_of_user(user_id, db: Session = Depends(get_db)):
    return db_queries.get_groups_of_user(db, user_id)
