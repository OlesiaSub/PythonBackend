from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.db_models import Expense, User, Group, UserGroupRelations
from model import tracker_model
from use_case.auth_logic import pwd_context


def create_expense(db: Session, expense: tracker_model.Expense):
    db_expense = Expense(name=expense.name,
                         expenditure=expense.expenditure,
                         date=expense.date,
                         category=expense.category,
                         description=expense.description,
                         expense_id=expense.expense_id,
                         user_id=expense.user_id,
                         group_id=expense.group_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db, user: tracker_model.User):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(user_id=user.user_id,
                   name=user.name,
                   gender=user.gender,
                   status=user.status,
                   hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_group(db, group: tracker_model.Group, participants: list[int]):
    db_group = Group(group_id=group.group_id,
                     name=group.name,
                     creator_id=group.creator_id,
                     description=group.description)
    if group.creator_id not in participants:
        participants.append(group.creator_id)
    for p in participants:
        if get_user_by_id(db, p) is None:
            raise HTTPException(status_code=404, detail="The user with id" + str(p) + "does not exist")

        db_relation = UserGroupRelations(group_id=group.group_id,
                                         user_id=p,
                                         user_is_admin=True)
        db.add(db_relation)
        db.commit()
        db.refresh(db_relation)

    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_user_expense_by_id(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(Expense.expense_id == expense_id
                                    and Expense.user_id == user_id).first()


def get_user_expenses(db: Session, user_id: int, limit: int = 100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(0).limit(limit).all()


def get_group_by_id(db: Session, group_id: int):
    return db.query(Group).filter(Group.group_id == group_id).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.name == user_name).first()


def get_group_expenses(db: Session, group_id: int, limit: int = 100):
    return db.query(Expense).filter(Expense.group_id == group_id).limit(limit).all()


def get_group_expenses_of_user(db: Session, group_id: int, user_id: int, limit: int = 100):
    return db.query(Expense).filter(Expense.group_id == group_id).filter(Expense.user_id == user_id).limit(limit).all()


def get_user_from_group(db: Session, group_id: int, limit: int = 100):
    return db.query(UserGroupRelations).filter(UserGroupRelations.group_id == group_id).limit(limit).all()


def get_groups_created_by_user(db: Session, user_id: int, limit: int = 100):
    return db.query(Group).filter(UserGroupRelations.user_id == user_id).filter(Group.creator_id == user_id) \
        .limit(limit).all()


def get_group_expenses_by_category(db: Session, group_id: int, category: str, limit: int = 100):
    return db.query(Expense).filter(Expense.group_id == group_id).filter(Expense.category == category) \
        .limit(limit).all()
