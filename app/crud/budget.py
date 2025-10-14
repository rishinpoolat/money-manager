from sqlalchemy.orm import Session
from ..models.budget import Budget
from ..schemas.budget import BudgetCreate, BudgetUpdate

def get_budgets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Budget).filter(Budget.user_id == user_id).offset(skip).limit(limit).all()

def get_budget_by_id(db: Session, budget_id: int, user_id: int):
    return db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()

def get_budget_by_category(db: Session, category_id: int, month: str, user_id: int):
    return db.query(Budget).filter(
        Budget.category_id == category_id,
        Budget.month == month,
        Budget.user_id == user_id
    ).first()

def create_budget(db: Session, budget: BudgetCreate, user_id: int):
    # Check if budget already exists for this category and month
    existing = get_budget_by_category(db, budget.category_id, budget.month, user_id)
    if existing:
        return None
    
    db_budget = Budget(**budget.dict(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, user_id: int, budget_update: BudgetUpdate):
    db_budget = get_budget_by_id(db, budget_id, user_id)
    if not db_budget:
        return None
    
    update_data = budget_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int, user_id: int):
    db_budget = get_budget_by_id(db, budget_id, user_id)
    if db_budget:
        db.delete(db_budget)
        db.commit()
        return True
    return False