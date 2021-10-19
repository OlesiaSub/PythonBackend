from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from model.tracker_model import Expense


def check_presence(expense_id: int, db: Session):
    return db_queries.get_expense_by_id(db, expense_id)


def check_available_storage(expense_id: int, db: Session):
    if check_presence(expense_id, db):
        raise HTTPException(status_code=400, detail="Expense with this id is already registered")
    else:
        return True


def validate_id(track_id: int):
    if track_id < 0:
        raise HTTPException(status_code=400, detail="Id is invalid, must be >= 0")
    else:
        return True


def validate_name(name: str):
    if name == '' or name == "" or not name.istitle() or name.isnumeric():
        raise HTTPException(status_code=400, detail="Name must start with capital, must not be empty or numeric")
    else:
        return True


def validate_expense(expense: Expense, db: Session):
    return validate_id(expense.expense_id) and validate_name(expense.name) \
           and check_available_storage(expense.expense_id, db)
