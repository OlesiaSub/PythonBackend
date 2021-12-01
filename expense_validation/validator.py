from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from model.tracker_model import Expense, Group


def check_expense_presence(expense_id: int, user_id: int, db: Session):
    return db_queries.get_user_expense_by_id(db, expense_id, user_id)


def check_user_id_presence(user_id: int, db: Session):
    return db_queries.get_user_by_id(db, user_id)


def check_user_name_presence(user_name: str, db: Session):
    return db_queries.get_user_by_name(db, user_name)


def check_available_storage_group_id(group_id: int, db: Session):
    if db_queries.get_group_by_id(db, group_id):
        raise HTTPException(status_code=400, detail="Group with this id is already registered")
    else:
        return True


def check_available_storage_expense_id(expense_id: int, user_id: int, db: Session):
    if check_expense_presence(expense_id, user_id, db):
        raise HTTPException(status_code=400, detail="Expense with this id is already registered")
    else:
        return True


def validate_id(track_id: int):
    if track_id < 0:
        raise HTTPException(status_code=400, detail="Id is invalid, must be >= 0")
    else:
        return True


def validate_expense_name(name: str):
    if name == '' or name == "" or not name.istitle() or name.isnumeric():
        raise HTTPException(status_code=400, detail="Name must start with capital, must not be empty or numeric")
    else:
        return True


# todo fix, add user check
def validate_expense(expense: Expense, db: Session):
    return validate_id(expense.expense_id) and validate_expense_name(expense.name) \
           and check_available_storage_expense_id(expense.expense_id, db)


def validate_is_admin(user_id: int, db: Session):
    return db_queries.get_user_by_id(db, user_id).is_admin


def validate_group(group: Group, db: Session):
    return validate_id(group.group_id) and \
           db_queries.get_user_by_id(db, group.creator_id).is_admin and \
           check_available_storage_group_id(group.group_id, db)
