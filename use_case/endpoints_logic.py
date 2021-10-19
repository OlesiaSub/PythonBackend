from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from expense_validation.validator import validate_id, validate_expense
from model.tracker_model import Expense


def process_get(expense_id: int, db: Session):
    id_int = int(expense_id)
    validate_id(id_int)
    db_expense = db_queries.get_expense_by_id(db, expense_id=id_int)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="This ID is not present in the database")
    return db_expense


def process_create_item(expense: Expense, db: Session):
    validate_expense(expense, db)
    return db_queries.create_user(db=db, expense=expense)
