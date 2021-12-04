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
    user_id = Column(Integer, ForeignKey('users.user_id'))
    group_id = Column(Integer, ForeignKey('groups.group_id'))


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    gender = Column(String)
    is_admin = Column(Boolean)
    status = Column(String)


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    creator_id = Column(Integer)
    description = Column(String)


class UserGroupRelations(Base):
    __tablename__ = "user_group_relations"

    relation_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user_is_admin = Column(Boolean, ForeignKey('users.is_admin'))
