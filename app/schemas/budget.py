from pydantic import BaseModel
from typing import Optional

class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: str  # Format: "YYYY-MM"

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    month: Optional[str] = None

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True