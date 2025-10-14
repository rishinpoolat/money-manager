from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime
    user_id: int
    
    class Config:
        from_attributes = True