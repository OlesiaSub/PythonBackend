from model.tracker_model import Expense

expense_storage = {}


def check_presence(expense: Expense):
    return expense.id in expense_storage
