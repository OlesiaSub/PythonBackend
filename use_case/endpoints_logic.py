from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import db_queries
from expense_validation.validator import validate_id, validate_group, validate_expense, validate_user, validate_category
from model.tracker_model import Expense, Group, User


def process_get_user_expense_by_id(expense_id: int, db: Session, current_user: User):
    if not current_user:
        return None
    expense_id_int = int(expense_id)
    user_id_int = int(current_user.user_id)
    validate_id(expense_id_int)
    validate_id(user_id_int)
    db_expense = db_queries.get_user_expense_by_id(db, expense_id=expense_id_int, user_id=current_user.user_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="This user's expense ID is not present in the database")
    return db_expense


def process_create_expense(expense: Expense, db: Session, current_user: User):
    if expense.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Trying to create expense of a user with another id")
    validate_expense(expense, db)
    return db_queries.create_expense(db=db, expense=expense)


def process_register_user(user: User, db: Session):
    validate_user(user, db)
    return db_queries.create_user(db=db, user=user)


def process_get_group(group_id: int, db: Session):
    id_int = int(group_id)
    validate_id(id_int)
    db_group = db_queries.get_group_by_id(db, group_id=id_int)
    if db_group is None:
        raise HTTPException(status_code=404, detail="This group is not present in the database")
    return db_group


def process_create_group(group: Group, participants_ids: list[int], db: Session, current_user: User):
    validate_group(group, db)
    if group.creator_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Only current user can be creator of a group")
    for p in participants_ids:
        validate_id(p)
    return db_queries.create_group(db, group=group, participants=participants_ids)


def process_get_group_expenses(group_id: int, db: Session, current_user: User):
    if db_queries.get_group_by_id(db, group_id).creator_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Current user is not this group's admin")
    return db_queries.get_group_expenses(db, group_id)


def process_get_user_expenses(db: Session, current_user: User):
    expenses = list(map(lambda expense: Expense(name=expense.name,
                                                expenditure=expense.expenditure,
                                                date=expense.date,
                                                category=expense.category,
                                                description=expense.description,
                                                expense_id=expense.expense_id,
                                                user_id=expense.user_id,
                                                group_id=expense.group_id),
                        db_queries.get_user_expenses(db, user_id=current_user.user_id, limit=100)))
    return expenses


def process_get_group_expenses_by_category(group_id, category, db: Session, current_user: User):
    if db_queries.get_group_by_id(db, group_id).creator_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Current user is not this group's admin")
    validate_category(category)
    return db_queries.get_group_expenses_by_category(db, group_id, category)
