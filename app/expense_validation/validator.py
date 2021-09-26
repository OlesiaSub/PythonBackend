from fastapi import HTTPException

from model.tracker_model import Expense
from storage.storage import check_presence


def check_available_storage(expense_id: int):
    if check_presence(expense_id):
        raise HTTPException(status_code=400, detail="This id already exists")
    else:
        return True


def validate_id(track_id: int):
    if track_id < 0:
        raise HTTPException(status_code=400, detail="ID is invalid, must be >= 0")
    else:
        return True


def validate_name(name: str):
    if name == '' or name == "" or not name.istitle() or name.isnumeric():
        raise HTTPException(status_code=400, detail="Name must start with capital, must not be empty or numeric")
    else:
        return True


def validate_expense(expense: Expense):
    return check_available_storage(expense.expense_id) \
           and validate_id(expense.expense_id) and validate_name(expense.name)
