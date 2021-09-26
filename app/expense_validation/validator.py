from fastapi import HTTPException

from model.tracker_model import Expense
from storage.storage import check_presence


def check_available_storage(expense: Expense):
    if check_presence(expense):
        raise HTTPException(status_code=400, detail="This id already exists")
    else:
        return True


def validate_id(track_id: int):
    if track_id < 0:
        raise HTTPException(status_code=400, detail="ID is invalid, must be >= 0")
    else:
        return True


def validate_name(name: str):
    if name == '' or name == "" or not name.istitle():
        raise HTTPException(status_code=400, detail="Name is invalid, must start with capital, must not be empty")
    else:
        return True


def validate_expense(expense: Expense):
    return check_available_storage(expense) and validate_id(expense.id) and validate_name(expense.name)
