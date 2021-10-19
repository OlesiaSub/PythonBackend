from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expenditure = Column(Integer)
    date = Column(DateTime)
    category = Column(String)
    description = Column(String)

