from fastapi import APIRouter, HTTPException

from model.tracker_model import Expense
from expense_validation.validator import validate_expense, validate_id
from storage import storage

router = APIRouter()


@router.get("/expenses_tracker/{expense_id}")
async def get_expense_id(expense_id):
    validate_id(expense_id)
    if not storage.check_presence(expense_id):
        raise HTTPException(status_code=400, detail="This id is not present in the storage.")
    return storage.expense_storage[expense_id]


@router.post("/expenses/")
async def create_item(expense: Expense):
    validate_expense(expense)
    storage.add_item(expense)
    return expense
