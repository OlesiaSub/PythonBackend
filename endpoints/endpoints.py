from fastapi import APIRouter, HTTPException

from model.tracker_model import Expense
from expense_validation.validator import validate_expense, validate_id
from storage import storage

router = APIRouter()


@router.get("/expenses_tracker/{expense_id}")
async def get_expense_id(expense_id):
    id_int = int(expense_id)
    validate_id(id_int)
    if not storage.check_presence(id_int):
        raise HTTPException(status_code=400, detail="This id is not present in the storage.")
    return storage.expense_storage[id_int]


@router.post("/expenses/")
async def create_item(expense: Expense):
    validate_expense(expense)
    storage.add_item(expense)
    return expense
