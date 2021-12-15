from array import array

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from model.tracker_model import Expense, Group, User

categories = {"Food", "Clothes", "Transport", "Medical", "Leisure", "Other"}


def check_expense_presence(expense_id: int, user_id: int, db: Session):
    return db_queries.get_user_expense_by_id(db, expense_id, user_id)


def check_user_id_presence(user_id: int, db: Session):
    return db_queries.get_user_by_id(db, user_id)


def check_user_presence(user_id: int, user_name: str, db: Session):
    return db_queries.get_user_by_name(db, user_name) or db_queries.get_user_by_id(db, user_id)


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


def check_available_storage_user(user_id: int, user_name: str, db: Session):
    if check_user_presence(user_id, user_name, db):
        raise HTTPException(status_code=400, detail="This user is already registered")
    else:
        return True


def validate_id(track_id: int):
    if track_id < 0:
        raise HTTPException(status_code=400, detail="Id is invalid, must be >= 0")
    else:
        return True


def validate_expense_name(name: str):
    if name == '' or name == "" or name.isnumeric():
        raise HTTPException(status_code=400, detail="Expense name must not be empty or numeric")
    else:
        return True


def validate_user_name(name: str):
    if name == '' or name == "" or name.isnumeric() or not name.istitle():
        raise HTTPException(status_code=400, detail="User name must not be empty or numeric, must start with capital")
    else:
        return True


def validate_user_gender(gender: str):
    if gender != "male" and gender != "female" and gender != "not stated":
        raise HTTPException(status_code=400,
                            detail="Invalid gender, put \"not stated\" if you don't want to specify it")
    else:
        return True


def validate_category(category: str):
    if category not in categories:
        raise HTTPException(status_code=400,
                            detail="Invalid category.\n List of available categories: " + str(categories))
    else:
        return True


def validate_expense(expense: Expense, db: Session):
    return validate_id(expense.expense_id) and validate_expense_name(expense.name) \
           and check_available_storage_expense_id(expense.expense_id, expense.user_id, db) \
           and validate_category(expense.category)


def validate_user(user: User, db: Session):
    return validate_id(user.user_id) and validate_user_name(user.name) and validate_user_gender(user.gender) \
           and check_available_storage_user(user.user_id, user.name, db)


def validate_group(group: Group, db: Session):
    return validate_id(group.group_id) and \
           check_available_storage_group_id(group.group_id, db)
