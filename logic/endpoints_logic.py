from fastapi import HTTPException

from expense_validation.validator import validate_id, validate_expense
from model.tracker_model import Expense
from storage import storage


def process_get(expense_id: int):
    id_int = int(expense_id)
    validate_id(id_int)
    if not storage.check_presence(id_int):
        raise HTTPException(status_code=400, detail="This ID is not present in the storage.")
    return storage.expense_storage[id_int]


def process_create_item(expense: Expense):
    validate_expense(expense)
    storage.add_item(expense)
    return expense
