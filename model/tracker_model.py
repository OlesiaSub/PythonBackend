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
