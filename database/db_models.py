from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expenditure = Column(Integer)
    date = Column(DateTime)
    category = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    # user_id = relationship("Child", back_populates="parent")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # validate
    gender = Column(String)
    is_admin = Column(Boolean)
    status = Column(String)  # like desc


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    creator_id = Column(Integer)
    description = Column(String)


class UserGroupRelations(Base):
    __tablename__ = "user_group_relations"

    group_id = Column(Integer, ForeignKey('groups.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user_is_admin = Column(Boolean, ForeignKey('users.is_admin'))


# maybe не нужна
class ExpenseGroupRelations(Base):
    __tablename__ = "expense_group_relations"

    group_id = Column(Integer, ForeignKey('groups.id'))
    expense_id = Column(Integer, ForeignKey('expenses.id'))