from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import db_queries
from database.database import get_db
from model import tracker_model
from model.tracker_model import Expense, User, Group, Token
from use_case.auth_logic import get_current_user, \
    process_get_access_token
from use_case.endpoints_logic import process_create_expense, process_get_group, \
    process_get_user_expense_by_id, process_create_group, process_register_user, process_get_group_expenses

router = APIRouter()


@router.post("/expenses/new_expense")
async def create_expense(expense: Expense, db: Session = Depends(get_db)):
    return process_create_expense(expense, db)


@router.post("/expenses/new_user")
async def create_user(user: User, db: Session = Depends(get_db)):
    return process_register_user(user, db)


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
async def get_group_expenses(group_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return process_get_group_expenses(group_id, db, current_user)


@router.get("/groups/{group_id}/{user_id}/expenses")
async def get_group_expenses_of_user(group_id, user_id, db: Session = Depends(get_db)):
    return db_queries.get_group_expenses_of_user(db, group_id, user_id)


@router.get("/user/{user_id}/groups")
async def get_groups_created_by_user(user_id, db: Session = Depends(get_db)):
    return db_queries.get_groups_created_by_user(db, user_id)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = process_get_access_token(form_data, db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/cabinet/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
