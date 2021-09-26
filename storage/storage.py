from model.tracker_model import Expense

expense_storage = {}


def check_presence(expense_id: int):
    return expense_id in expense_storage.keys()


def add_item(expense: Expense):
    expense_storage[expense.expense_id] = expense
