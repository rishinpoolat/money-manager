from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from ..crud import budget as crud_budget
from ..crud import category as crud_category
from .auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.get("/", response_model=List[BudgetResponse])
def get_budgets(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_budget.get_budgets(db, current_user.id, skip, limit)

@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget: BudgetCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify category belongs to user
    category = crud_category.get_category_by_id(db, budget.category_id, current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if budget already exists for this category and month
    existing = crud_budget.get_budget_by_category(db, budget.category_id, budget.month, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category and month")
    
    db_budget = crud_budget.create_budget(db, budget, current_user.id)
    if not db_budget:
        raise HTTPException(status_code=400, detail="Failed to create budget")
    
    return db_budget

@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budget = crud_budget.get_budget_by_id(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    budget = crud_budget.update_budget(db, budget_id, current_user.id, budget_update)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = crud_budget.delete_budget(db, budget_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget not found")
    return None