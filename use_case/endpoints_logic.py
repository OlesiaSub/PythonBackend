from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from expense_validation.validator import validate_id, validate_group
from model.tracker_model import Expense, Group, User


def process_get_user_expense_by_id(user_id: int, expense_id: int, db: Session):
    expense_id_int = int(expense_id)
    user_id_int = int(user_id)
    validate_id(expense_id_int)
    validate_id(user_id_int)
    db_expense = db_queries.get_user_expense_by_id(db, expense_id=expense_id_int, user_id=user_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="This user's expense ID is not present in the database")
    return db_expense


def process_create_expense(expense: Expense, db: Session):
    # todo:
    #  validate expense
    # validate_expense(expense, db)
    return db_queries.create_expense(db=db, expense=expense)


def process_create_user(user: User, db: Session):
    return db_queries.create_user(db=db, user=user)


def process_get_group(group_id: int, db: Session):
    id_int = int(group_id)
    validate_id(id_int)
    db_group = db_queries.get_group_by_id(db, group_id=id_int)
    if db_group is None:
        raise HTTPException(status_code=404, detail="This group is not present in the database")
    return db_group


def process_create_group(group: Group, participants_ids, db: Session):
    validate_group(group, db)
    return db_queries.create_group(db, group=group)
