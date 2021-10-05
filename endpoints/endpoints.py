from fastapi import APIRouter

from logic.endpoints_logic import process_get, process_create_item
from model.tracker_model import Expense

router = APIRouter()


@router.get("/expenses_tracker/{expense_id}")
async def get_expense_id(expense_id):
    # id_int = int(expense_id)
    # validate_id(id_int)
    # if not storage.check_presence(id_int):
    #     raise HTTPException(status_code=400, detail="This id is not present in the storage.")
    # return storage.expense_storage[id_int]
    return process_get(expense_id)


@router.post("/expenses/")
async def create_item(expense: Expense):
    return process_create_item(expense)
