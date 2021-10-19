from sqlalchemy.orm import Session

from model import tracker_model
from database import db_models


def get_expense_by_id(db: Session, expense_id: int):
    return db.query(db_models.Expense).filter(db_models.Expense.expense_id == expense_id).first()


def get_expense_by_name(db: Session, name: str):
    return db.query(db_models.Expense).filter(db_models.Expense.name == name).first()


def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Expense).offset(skip).limit(limit).all()


def create_user(db: Session, expense: tracker_model.Expense):
    db_expense = db_models.Expense(name=expense.name,
                                   expenditure=expense.expenditure,
                                   date=expense.date,
                                   category=expense.category,
                                   description=expense.description,
                                   expense_id=expense.expense_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
