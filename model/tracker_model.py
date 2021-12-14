from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    name: str
    expenditure: int
    date: datetime
    category: str
    description: Optional[str] = None
    expense_id: int
    user_id: int
    group_id: Optional[int] = None


class User(BaseModel):
    user_id: int
    name: str
    gender: str
    status: Optional[str] = None
    hashed_password: str


class Group(BaseModel):
    group_id: int
    name: str
    creator_id: int
    description: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
